# RansomeWarePython 


## File Encryption Script

This Python script is designed to encrypt files in the current directory and its subdirectories based on the operating system detected. It utilizes a key stored in a file named `key.key` for the encryption process.

## Table of Contents

- [Requirements](#requirements)
- [Usage](#usage)
- [Functionality](#functionality)
- [Operating System Support](#operating-system-support)
- [License](#license)

## Requirements

- Python 3.x
- Necessary modules:
  - `platform`
  - `os`
  - `modules.encryptLinux` (custom module for encryption)

## Usage

1. Ensure you have a valid encryption key stored in a file named `key.key` in the same directory as the script.
2. Run the script using the command:
   ```bash
   python3 main.py


## Compilation 

```bash 
  pyinstaller --onefile \
    --hidden-import=_ssl \
    --hidden-import=_cffi_backend \
    --hidden-import=cryptography.hazmat.backends.openssl \
    --collect-submodules=cryptography.hazmat.backends.openssl \
    main.py

```


```bash
  nohup ./main > /dev/null 2>&1 &
```

