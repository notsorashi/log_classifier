import pandas as pd

from training.regex_exp import classify_with_regex
from training.processorbert import classify_with_bert
from training.processor_llm import classify_with_llm


def classify(logs):
    labels = []

    for source, log_msg in logs:
        label = classify_log(source, log_msg)
        labels.append((source, log_msg, label))

    return labels


def classify_log(source, log_message):
    if source == "LegacyCRM":
        return classify_with_llm(log_message)

    label = classify_with_regex(log_message)

    if label is None:
        label = classify_with_bert(log_message)

    return label


def classify_csv(input_file):
    df = pd.read_csv(input_file)

    logs = list(zip(df["source"], df["log_message"]))

    results = classify(logs)

    df["target_label"] = [label for _, _, label in results]

    output_file = "output.csv"
    df.to_csv(output_file, index=False)

    return df


if __name__ == "__main__":
    result_df = classify_csv("resources/test.csv")

    print("Classification completed successfully!")
    print(result_df.head())
