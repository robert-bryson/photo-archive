mod commands;

use clap::{Parser, Subcommand};
use commands::archive;
use commands::check;

#[derive(Parser, Debug)]
#[command(author, version, about = "PHoto Archive Tool", long_about = None)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand, Debug)]
enum Commands {
    #[command(
        about = "Checks input directory",
        long_about = "Checks the specified input directory for photos and displays relevant information."
    )]
    Check {
        #[arg(help = "Specify the input directory to check")]
        input_dir: String,
    },
    #[command(
        about = "Archives photos",
        long_about = "Archives photos to the specified destination directory, applying compression if necessary."
    )]
    Archive {
        #[arg(short = 's', long, help = "Specify the source directory")]
        src_dir: String,
        #[arg(short = 'd', long, help = "Specify the destination directory")]
        dest_dir: String,
    },
}

fn main() {
    let cli = Cli::parse();

    match &cli.command {
        Commands::Check { input_dir } => check::execute(input_dir),
        Commands::Archive { src_dir, dest_dir } => match archive::execute(src_dir, dest_dir) {
            Ok(stats) => println!("Archive completed successfully: {:?}", stats),
            Err(e) => eprintln!("Failed to archive files: {}", e),
        },
    }
}
