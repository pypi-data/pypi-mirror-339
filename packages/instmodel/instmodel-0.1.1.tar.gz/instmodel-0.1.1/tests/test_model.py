from instmodel.model import (
    Attention,
    Concatenate,
    Dense,
    InputBuffer,
    ModelGraph,
    Add,
    ff_model,
    create_instruction_model,
    create_model_graph,
    validate_keras_model,
    NOT_INPLACE,
    NO_BATCH_NORM,
)


from instmodel.instruction_model import (
    validate_instruction_model,
    instruction_model_inference,
    generate_features,
)

import json
import numpy as np
import pandas as pd


def test_simple_dense_model():
    """
    Tests a simple feed-forward model with three Dense layers:
      - The first Dense uses ReLU activation.
      - The second Dense uses ReLU activation.
      - The third Dense uses Sigmoid activation.
    Then validates that the exported instruction model matches the Keras outputs.
    """

    input_buffer = InputBuffer(4, name="simple_input")
    hidden = Dense(8, activation="relu", name="hidden_relu_1")(input_buffer)
    hidden = Dense(6, activation="relu", name="hidden_relu_2")(hidden)
    output = Dense(1, activation="sigmoid", name="output_sigmoid")(hidden)

    model_graph = ModelGraph(input_buffer, output)
    model_graph.compile(optimizer="adam", loss="binary_crossentropy")

    # Generate dummy data for demonstration.
    x_data = np.random.random((10, 4))
    y_data = np.random.randint(0, 2, size=(10, 1))  # random 0/1 labels

    # Train for one epoch.
    model_graph.fit(x_data, y_data, epochs=1, verbose=0)

    # Export the trained model to an instruction model.
    instruction_model = model_graph.create_instruction_model()

    # Compare Keras predictions to the instruction-model predictions.
    keras_pred = model_graph.predict(x_data, verbose=0)
    instruction_model["validation_data"] = {
        "inputs": x_data.tolist(),
        "expected_outputs": keras_pred.tolist(),
    }

    # Validate to ensure both models produce the same output.
    validate_instruction_model(instruction_model)
    validate_keras_model(model_graph.get_keras(), instruction_model["validation_data"])

    print(
        "Simple Dense model validation successful: Instruction model matches Keras output."
    )

    del instruction_model["weights"]
    del instruction_model["bias"]
    del instruction_model["parameters"]
    del instruction_model["maps"]
    del instruction_model["validation_data"]

    # If you want to test the exact instruction set, you can assert something like:
    assert instruction_model["buffer_sizes"] == [4, 8, 6, 1]
    assert instruction_model["instructions"] == [
        {"type": "DOT", "input": 0, "output": 1, "weights": 0, "activation": "RELU"},
        {"type": "DOT", "input": 1, "output": 2, "weights": 1, "activation": "RELU"},
        {"type": "DOT", "input": 2, "output": 3, "weights": 2, "activation": "SIGMOID"},
    ]

    # This is the compact format to create a simple feed-forward model.
    model_graph_copy = ff_model([4, 8, 6, 1], NO_BATCH_NORM, "rrs")

    instruction_model_copy = model_graph_copy.create_instruction_model()

    del instruction_model_copy["weights"]
    del instruction_model_copy["bias"]
    del instruction_model_copy["parameters"]
    del instruction_model_copy["maps"]

    assert instruction_model_copy == instruction_model


def test_complex_attention_model():
    """
    Tests a complex attention-based model and validates both the instruction model and Keras model.
    """
    i_target = InputBuffer(20, name="target")
    i_key = Dense(10, name="key_dense")(i_target)
    attn = Attention(name="attention")
    attn_out = attn([i_target, i_key])
    d_out = Dense(1, activation="sigmoid", name="dense_output")(attn_out)

    model_graph = create_model_graph(i_target, d_out)

    model_graph.compile(optimizer="adam", loss="mse")
    x_data = np.random.random((50, 20))
    y_data = np.random.random((50, 1))
    model_graph.fit(x_data, y_data, epochs=2, verbose=0)

    result = create_instruction_model(i_target, d_out)

    keras_pred = model_graph.predict(x_data, verbose=0)
    result["validation_data"] = {
        "inputs": x_data.tolist(),
        "expected_outputs": keras_pred.tolist(),
    }

    validate_instruction_model(result)
    validate_keras_model(model_graph.get_keras(), result["validation_data"])

    print("Validation successful: Instruction model output matches expected output.")

    del result["weights"]
    del result["bias"]
    del result["parameters"]
    del result["maps"]
    del result["validation_data"]

    assert result == {
        "features": [],
        "buffer_sizes": [20, 10, 20, 1],
        "instructions": [
            {"type": "DOT", "input": 0, "output": 1, "weights": 0},
            {"type": "ATTENTION", "input": 0, "key": 1, "output": 2, "weights": 1},
            {
                "type": "DOT",
                "input": 2,
                "output": 3,
                "weights": 2,
                "activation": "SIGMOID",
            },
        ],
    }


def test_nested_model():
    """
    Tests a nested model structure and validates the resulting instruction model.
    """
    model = ff_model([3, 3, 3], NOT_INPLACE, "ll")

    main_input = InputBuffer(3)

    first_iteration = model(main_input)
    second_iteration = model(first_iteration)

    concat = Concatenate()([main_input, first_iteration, second_iteration])

    dense_out = Dense(1)(concat)

    final_model = ModelGraph(main_input, dense_out)

    final_model.compile(optimizer="adam", loss="mse")
    x_data = np.random.random((50, 3)) + 2
    y_data = np.random.random((50, 1))

    final_model.fit(x_data, y_data, epochs=1, verbose=0)
    result = final_model.create_instruction_model()

    y_pred = final_model.predict(x_data)

    result["validation_data"] = {
        "inputs": x_data.tolist(),
        "expected_outputs": y_pred.tolist(),
    }

    validate_instruction_model(result)
    validate_keras_model(final_model.get_keras(), result["validation_data"])

    del result["weights"]
    del result["bias"]
    del result["parameters"]
    del result["maps"]
    del result["validation_data"]

    assert result == {
        "features": [],
        "buffer_sizes": [3, 3, 3, 3, 3, 3, 3, 9, 1],
        "instructions": [
            {"type": "COPY", "input": 0, "output": 1, "internal_index": 0},
            {"type": "ADD_ELEMENTWISE", "input": 1, "parameters": 0},
            {"type": "MUL_ELEMENTWISE", "input": 1, "parameters": 1},
            {"type": "ADD_ELEMENTWISE", "input": 1, "parameters": 2},
            {"type": "DOT", "input": 1, "output": 2, "weights": 0},
            {"type": "DOT", "input": 2, "output": 3, "weights": 1},
            {"type": "COPY", "input": 3, "output": 4, "internal_index": 0},
            {"type": "ADD_ELEMENTWISE", "input": 4, "parameters": 0},
            {"type": "MUL_ELEMENTWISE", "input": 4, "parameters": 1},
            {"type": "ADD_ELEMENTWISE", "input": 4, "parameters": 2},
            {"type": "DOT", "input": 4, "output": 5, "weights": 0},
            {"type": "DOT", "input": 5, "output": 6, "weights": 1},
            {"type": "COPY", "input": 0, "output": 7, "internal_index": 0},
            {"type": "COPY", "input": 3, "output": 7, "internal_index": 3},
            {"type": "COPY", "input": 6, "output": 7, "internal_index": 6},
            {"type": "DOT", "input": 7, "output": 8, "weights": 2},
        ],
    }


def test_ff_models():
    """
    Tests composite feed-forward models with concatenation and validates the instruction model.
    """
    input_buffer = InputBuffer(3)

    path1 = ff_model([3, 5, 3], NOT_INPLACE, "rs")(input_buffer)

    path2 = ff_model([3, 4, 6], NOT_INPLACE, "tr")(input_buffer)

    concat = Concatenate()([path1, path2])

    out = ff_model([concat.os, 2, 1], NO_BATCH_NORM, "ts")(concat)

    final_model = ModelGraph(input_buffer, out)

    result = final_model.create_instruction_model()

    del result["weights"]
    del result["bias"]
    del result["parameters"]
    del result["maps"]

    assert result == {
        "features": [],
        "buffer_sizes": [3, 3, 5, 3, 3, 4, 6, 9, 2, 1],
        "instructions": [
            {"type": "COPY", "input": 0, "output": 1, "internal_index": 0},
            {"type": "ADD_ELEMENTWISE", "input": 1, "parameters": 0},
            {"type": "MUL_ELEMENTWISE", "input": 1, "parameters": 1},
            {"type": "ADD_ELEMENTWISE", "input": 1, "parameters": 2},
            {
                "type": "DOT",
                "input": 1,
                "output": 2,
                "weights": 0,
                "activation": "RELU",
            },
            {
                "type": "DOT",
                "input": 2,
                "output": 3,
                "weights": 1,
                "activation": "SIGMOID",
            },
            {"type": "COPY", "input": 0, "output": 4, "internal_index": 0},
            {"type": "ADD_ELEMENTWISE", "input": 4, "parameters": 3},
            {"type": "MUL_ELEMENTWISE", "input": 4, "parameters": 4},
            {"type": "ADD_ELEMENTWISE", "input": 4, "parameters": 5},
            {
                "type": "DOT",
                "input": 4,
                "output": 5,
                "weights": 2,
                "activation": "TANH",
            },
            {
                "type": "DOT",
                "input": 5,
                "output": 6,
                "weights": 3,
                "activation": "RELU",
            },
            {"type": "COPY", "input": 3, "output": 7, "internal_index": 0},
            {"type": "COPY", "input": 6, "output": 7, "internal_index": 3},
            {
                "type": "DOT",
                "input": 7,
                "output": 8,
                "weights": 4,
                "activation": "TANH",
            },
            {
                "type": "DOT",
                "input": 8,
                "output": 9,
                "weights": 5,
                "activation": "SIGMOID",
            },
        ],
    }


def test_slices():
    """
    Tests slicing of an InputBuffer and the concatenation of sliced outputs.
    """
    input_buffer = InputBuffer(3)

    slice1 = input_buffer[1:]
    slice2 = input_buffer[:1]

    concat = Concatenate()([slice1, slice2])

    model = ModelGraph(input_buffer, concat)

    result = model.create_instruction_model()

    del result["weights"]
    del result["bias"]
    del result["parameters"]
    del result["maps"]

    assert result == {
        "features": [],
        "buffer_sizes": [3, 2, 1, 3],
        "instructions": [
            {"type": "COPY_MASKED", "input": 0, "output": 1, "indexes": [1, 2]},
            {"type": "COPY_MASKED", "input": 0, "output": 2, "indexes": [0]},
            {"type": "COPY", "input": 1, "output": 3, "internal_index": 0},
            {"type": "COPY", "input": 2, "output": 3, "internal_index": 2},
        ],
    }


def test_feature_computing():
    """
    Tests the feature computing functionality of the model.
    """
    input_buffers = [InputBuffer(1), InputBuffer(1)]

    output = Add()(input_buffers)

    model = ModelGraph(input_buffers, output)

    inst_model = model.create_instruction_model(None, ["feature1", "feature2"])

    with open("tests/files/instmodel.json", "r") as f:
        file_content = json.load(f)

    assert file_content == inst_model

    result = instruction_model_inference(inst_model, [np.array([[1]]), np.array([[2]])])

    assert result[0] == 1
    assert result[1] == 2
    assert result[2] == 3

    # Create a DataFrame with the specified dataset.
    simple_dataset = pd.DataFrame({"feature1": [1, 0.5], "feature2": [2, -5.0]})

    simple_dataset = generate_features(
        "tests/files/instmodel.json", simple_dataset, ["feature3"]
    )

    assert simple_dataset.columns.tolist() == ["feature1", "feature2", "feature3"]

    assert simple_dataset["feature3"].tolist() == [3, -4.5]
