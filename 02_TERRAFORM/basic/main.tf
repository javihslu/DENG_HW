terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

provider "google" {
# Credentials only needs to be set if you do not have the GOOGLE_APPLICATION_CREDENTIALS set
  credentials = "../../keys/gcp_service_key.json"
  project = "dengtaxi-489313"
  region  = "EU"
}



resource "google_storage_bucket" "deng_jvr_bucket" {
  name          = "deng_jvr_bucket_terraform"
  location      = "EU"

  # Optional, but recommended settings:
  storage_class = "STANDARD"
  uniform_bucket_level_access = true

  versioning {
    enabled     = true
  }

  lifecycle_rule {
    action {
      type = "AbortIncompleteMultipartUpload"
    }
    condition {
      age = 30  // days
    }
  }

  force_destroy = true
}


resource "google_bigquery_dataset" "dataset" {
  dataset_id = "DENG_TAXI_Demo"
  project    = "dengtaxi-489313"
  location   = "EU"
}