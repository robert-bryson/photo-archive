use chrono::{DateTime, Utc};
use exif::{Exif, Reader as ExifReader};
use std::collections::HashMap;
use std::fs::File;
use std::path::{Path, PathBuf};
use walkdir::WalkDir;

pub struct PhotoStats {
    pub total_files: usize,
    pub total_dirs: usize,
    pub format_counts: HashMap<String, usize>,
    pub first_date: Option<DateTime<Utc>>,
    pub last_date: Option<DateTime<Utc>>,
    pub photo_with_metadata: usize,
    pub cameras: HashMap<String, usize>,
}

impl PhotoStats {
    pub fn new() -> Self {
        PhotoStats {
            total_files: 0,
            total_dirs: 0,
            format_counts: HashMap::new(),
            first_date: None,
            last_date: None,
            photo_with_metadata: 0,
            cameras: HashMap::new(),
        }
    }
}

// Main public function(s) that use the above types
pub fn execute(input_dir: &str) {
    println!("Checking directory: {}", input_dir);

    let src_dir = PathBuf::from(input_dir);

    check_photos(src_dir);
}

pub fn check_photos(input_dir: &Path) -> Result<PhotoStats, std::io::Error> {
    let mut stats = PhotoStats::new();
    for entry in WalkDir::new(input_dir) {
        let entry = entry?;
        let path = entry.path();
        if path.is_dir() {
            stats.total_dirs += 1;
            continue;
        }

        let extension = path
            .extension()
            .map_or("".to_string(), |e| e.to_string_lossy().to_lowercase());

        match extension.as_str() {
            "jpg" | "jpeg" | "png" | "gif" | "bmp" | "tiff" => {
                stats.total_files += 1;
                *stats.format_counts.entry(extension).or_insert(0) += 1;

                if let Ok(file) = File::open(path) {
                    let mut bufreader = std::io::BufReader::new(file);
                    if let Ok(exif) = ExifReader::new().read_from_container(&mut bufreader) {
                        stats.photo_with_metadata += 1;
                        if let Some(field) = exif.get_field(exif::Tag::Model, exif::In::PRIMARY) {
                            let camera_name = field.value.display_as(exif::Tag::Model).to_string();
                            *stats.cameras.entry(camera_name).or_insert(0) += 1;
                        }
                    }
                }
            }
            _ => {}
        }
    }
    Ok(stats)
}
