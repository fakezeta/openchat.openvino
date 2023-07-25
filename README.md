# llama2.openvino
This sample shows how to implement a llama-based model with OpenVINO runtime.

<img width="947" alt="MicrosoftTeams-image (2)" src="https://github.com/OpenVINO-dev-contest/llama2.openvino/assets/91237924/c210507f-1fb2-4c68-a8d9-dae945df07d3">


- ***Please follow the Licence on HuggingFace and get the approval from Meta before downloading llama checkpoints, for more [information](https://huggingface.co/meta-llama/Llama-2-7b-hf)***

- ***Please notice this repository is only for a functional test and personal study, and you can try to quantize the model to further optimize the performance of it***

## How to run it?
1. Install the requirements:

    ```python3 -m venv openvino_env```

    ```source openvino_env/bin/activate```

    ```$pip install -r requirements.txt```


### Option 1: OpenVINO IR pipeline, export IR model from HF Optimum-Intel
2. Run [Optimum-Intel OpenVINO pipeline](https://huggingface.co/docs/optimum/intel/inference) and export the IR model

    ```$python3 export_ir.py -m 'meta-llama/Llama-2-7b-chat-hf' -o './ir_model'```

    ```$cd ir_pipeline```

    ```$python3 generate_op.py -m "meta-llama/Llama-2-7b-hf" -p "what is openvino ?" -d "CPU"``` 

3. (Optional) Run restructured pipeline:

    ```$python3 generate_ir.py -m "meta-llama/Llama-2-7b-hf" -p "what is openvino ?" -d "CPU"```


### Option 2: ONNX pipeline, export ONNX model from HF Optimum

2. Export the ONNX model from HuggingFace Optimum and convert it to OpenVINO IR:

    ```$cd onnx_pipeline```

    ```$optimum-cli export onnx --model meta-llama/Llama-2-7b-hf ./onnx_model/```

    ```$mkdir ir_model```

    ```$mo -m ./onnx_model/decoder_model_merged.onnx -o ./ir_model/ --compress_to_fp16```

    ```$rm ./onnx_model/ -rf```

3. Run restructured pipeline:

    ```$python3 generate_onnx.py -m  "meta-llama/Llama-2-7b-hf" -p "what is openvino ?" -d "CPU"```


### Option 3: Interactive demo

2. Run interactive Q&A demo with Gradio

    ```$cd demo```

    ```$python3 qa_gradio.py -m "meta-llama/Llama-2-7b-hf" ```

2. or Chat Robot demo with Streamlit

    ```python3 export_ir.py -m 'meta-llama/Llama-2-7b-chat-hf' -o './ir_model_chat'```

    ```$cd demo```

    ```$streamlit run chat_streamlit.py```
