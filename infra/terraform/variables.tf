variable "resource_group_name" {
  default     = "rg-medical-analytics"
}

variable "location" {
  default     = "East US" 
}

variable "admin_username" {
  default     = "azureuser"
}

variable "admin_password" {
  sensitive   = true
}