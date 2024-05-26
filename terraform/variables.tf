variable "credentials_file_path" {
  description = "value of the credentials file"
  default     = "../keys/easytour-422214-f766b76f94d1.json"

}

variable "project" {
  description = "project"
  default     = "EasyTour"

}

variable "region" {
  description = "Project region name"
  default     = "us-central1"

}


variable "location" {
  description = "Project location name"
  default     = "US"

}

variable "bq_dataset_name" {
  description = "my bigquery dataset name"
  type        = string
  default     = "easy_tour_dataset"
}

variable "gcs_bucket_name" {
  description = "my storage bucket name"
  default     = "easy_tour_bucket"
}

variable "gcs_storage_class" {
  description = "bucket storage class"
  default     = "STANDARD"
}
