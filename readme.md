# Photo Archive Tool

The Photo Archive Tool is a Rust-based CLI application designed for archiving and managing digital photos. It allows users to transfer images from sources like SD cards to a structured destination directory on their computer. The tool supports zipping photos for compact storage and preparing subsets for cloud uploads.

## Features

- Transfer and organize photos from any directory.
- Compress photos into a ZIP file.
- Prepare photos for upload to services like Google Photos.

## Installation

Install Rust, clone the repository, and build the project:
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
git clone https://github.com/robert-bryson/photo-archive.git
cd photo-archive
cargo build --release
```

## Usage

Run the tool with the following command:

bash

`./target/release/photo_archive_tool --input <input_path> --dest <destination_path> [options]`

Options include:

    --zip to compress the photos.
    --prepare-upload to prepare photos for cloud uploading.

## License

Licensed under the MIT License.
