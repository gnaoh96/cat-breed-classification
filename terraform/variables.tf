// Variables to use accross the project
// which can be accessed by var.project_id
variable "project_id" {
  description = "The project ID to host the cluster in"
  default     = "st-project-416913"
}

variable "region" {
  description = "The region the cluster in"
  default     = "asia-southeast1"
}

variable "zone" {
  description = "The region the cluster in"
  default     = "asia-southeast1-a"
}

variable "self_link" {
  description = "The self_link of the network to attach this firewall to"
  default = "global/networks/default"
}
