use std::fs;
use std::path::Path;
use walkdir::WalkDir;

#[derive(Debug)]
pub struct ArchiveStats {
    pub total_files_moved: usize,
    pub total_dirs_created: usize,
}

impl ArchiveStats {
    pub fn new() -> Self {
        ArchiveStats {
            total_files_moved: 0,
            total_dirs_created: 0,
        }
    }
}

pub fn execute(src_dir: &str, dest_dir: &str) -> Result<ArchiveStats, std::io::Error> {
    let mut stats = ArchiveStats::new();
    let src_path = Path::new(src_dir);
    let dest_path = Path::new(dest_dir);

    // Ensure destination directory exists or create it
    if !dest_path.exists() {
        fs::create_dir_all(dest_path)?;
        stats.total_dirs_created += 1;
    }

    // Iterate over files in the source directory
    for entry in WalkDir::new(src_path).into_iter().filter_map(|e| e.ok()) {
        let file_path = entry.path();
        if file_path.is_file() {
            let rel_path = file_path.strip_prefix(src_path).unwrap();
            let target_path = dest_path.join(rel_path);

            // Ensure the target directory exists or create it
            if let Some(parent) = target_path.parent() {
                if !parent.exists() {
                    fs::create_dir_all(parent)?;
                    stats.total_dirs_created += 1;
                }
            }

            // Move the file
            fs::copy(file_path, &target_path)?;
            stats.total_files_moved += 1;
        }
    }

    Ok(stats)
}
