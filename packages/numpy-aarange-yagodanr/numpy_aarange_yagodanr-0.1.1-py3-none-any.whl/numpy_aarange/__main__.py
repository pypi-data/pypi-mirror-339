from .aarange import aarange


def main():
    """
    Main function to demonstrate the usage of the aarange function.
    """
    # Define the start, stop, and step values
    rang = 5
    size = 4

    # Call the aarange function and print the result
    result = aarange(rang, size)
    print(f"Result of aarange({rang}, {size}): \n{result}")

if __name__ == "__main__":
    main()
