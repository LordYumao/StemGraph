#!/usr/bin/env bash
if [ -n "$1" ]; then
    CONFIG_DIR="$1"
    if [ ! -d "$CONFIG_DIR" ]; then
        exit 1
    fi
    export ENV=$(basename "$CONFIG_DIR")
    export CONFIG_PATH="$CONFIG_DIR/config"
    if [ -f "${CONFIG_PATH}.json" ]; then
        export CONFIG_BACKEND="json"
    elif [ -f "${CONFIG_PATH}.toml" ]; then
        export CONFIG_BACKEND="toml"
    elif [ -f "${CONFIG_PATH}.env" ]; then
        export CONFIG_BACKEND="env"
    else
        exit 1
    fi
fi

if [ -z "${VENV_PATH}" ]; then
    if [ -n "${VIRTUAL_ENV}" ]; then
        export VENV_PATH="${VIRTUAL_ENV}"
    else
        export VENV_PATH="$(pwd)/.venv"
    fi
fi
if [ -z "${DISABLE_LD_OVERRIDE}" ]; then
    export NVJITLINK_PATH="$(find "${VENV_PATH}" -name nvjitlink -type d)/lib"
    if [ -n "${NVJITLINK_PATH}" ]; then
        export LD_LIBRARY_PATH="${NVJITLINK_PATH}:${LD_LIBRARY_PATH}"
    fi
fi

export TOKENIZERS_PARALLELISM=false
export PLATFORM
PLATFORM=$(uname -s)
if [[ "$PLATFORM" == "Darwin" ]]; then
    export MIXED_PRECISION="no"
fi

if [ -z "${ACCELERATE_EXTRA_ARGS}" ]; then
    ACCELERATE_EXTRA_ARGS=""
fi

if [ -z "${TRAINING_NUM_PROCESSES}" ]; then
    TRAINING_NUM_PROCESSES=1
fi

if [ -z "${TRAINING_NUM_MACHINES}" ]; then
    TRAINING_NUM_MACHINES=1
fi

if [ -z "${MIXED_PRECISION}" ]; then
    MIXED_PRECISION=bf16
fi

if [ -z "${TRAINING_DYNAMO_BACKEND}" ]; then
    TRAINING_DYNAMO_BACKEND="no"
fi

if [ -z "$1" ]; then
    if [ -z "${ENV}" ]; then
        export ENV="default"
    fi
    export ENV_PATH=""
    if [[ "$ENV" != "default" ]]; then
        export ENV_PATH="${ENV}/"
    fi

    if [ -z "${CONFIG_BACKEND}" ]; then
        if [ -n "${CONFIG_TYPE}" ]; then
            export CONFIG_BACKEND="${CONFIG_TYPE}"
        fi
    fi

    if [ -z "${CONFIG_BACKEND}" ]; then
        export CONFIG_BACKEND="env"
        export CONFIG_PATH="config/${ENV_PATH}config"
        if [ -f "${CONFIG_PATH}.json" ]; then
            export CONFIG_BACKEND="json"
        elif [ -f "${CONFIG_PATH}.toml" ]; then
            export CONFIG_BACKEND="toml"
        elif [ -f "${CONFIG_PATH}.env" ]; then
            export CONFIG_BACKEND="env"
        fi
    fi
fi

if [ -z "${DISABLE_UPDATES}" ]; then
    if [ -f "pyproject.toml" ] && [ -f "poetry.lock" ]; then
        nvidia-smi 2> /dev/null && poetry install
        uname -s | grep -q Darwin && poetry install -C install/apple
        rocm-smi 2> /dev/null && poetry install -C install/rocm
    fi
fi

if [[ -z "${ACCELERATE_CONFIG_PATH}" ]]; then
    if [[ -f "${HF_HOME}/accelerate/default_config.yaml" ]]; then
        ACCELERATE_CONFIG_PATH="${HF_HOME}/accelerate/default_config.yaml"
    else
        ACCELERATE_CONFIG_PATH="${HOME}/.cache/huggingface/accelerate/default_config.yaml"
    fi
fi
if [ -f "${ACCELERATE_CONFIG_PATH}" ]; then
    accelerate launch --config_file="${ACCELERATE_CONFIG_PATH}" train.py
else
    accelerate launch ${ACCELERATE_EXTRA_ARGS} --mixed_precision="${MIXED_PRECISION}" --num_processes="${TRAINING_NUM_PROCESSES}" --num_machines="${TRAINING_NUM_MACHINES}" --dynamo_backend="${TRAINING_DYNAMO_BACKEND}" train.py
fi

exit 0