
# You should not modify this part.
def config():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--consume", default="training_data.csv", help="input training data file name")
    parser.add_argument("--generate", default="testing_data.csv", help="input testing data file name")
    parser.add_argument("--output", default="output.csv", help="output file name")
    args = parser.parse_args()

if __name__ == "__main__":
    args = config()

    # You can write code above the if-main block.
    pass