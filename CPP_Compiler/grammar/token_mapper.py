import os

def read_tokens(file_path):
    with open(file_path, 'r') as file:
        tokens = []
        for line in file.readlines():
            # Strip whitespace and remove comments
            line = line.strip()
            if line and not line.startswith('//'):
                # Remove trailing comma and any comments
                token = line.split('//')[0].strip().rstrip(',')
                if token:
                    tokens.append(token)
    return tokens

def read_output(file_path):
    with open(file_path, 'r') as file:
        # Read all numbers and convert to integers
        numbers = [int(line.strip()) for line in file.readlines() if line.strip()]
    return numbers

def main():
    # Get the directory where this script is located
    base_dir = os.path.dirname(os.path.abspath(__file__))
    tok_path = os.path.join(base_dir, 'tok.txt')
    out_path = os.path.join(base_dir, 'output.txt')

    # Read the token definitions
    tokens = read_tokens(tok_path)
    
    # Read the output numbers
    numbers = read_output(out_path)
    
    # Map numbers to tokens (use index directly)
    token_sequence = [tokens[num] for num in numbers]
    
    # Print tokens, inserting a newline when 'NEWLINE' is encountered
    for token in token_sequence:
        if token == 'NEWLINE':
            print(token)
        else:
            print(token, end=' ')

if __name__ == "__main__":
    main() 