
terraform {
  required_version = ">= 0.14.0"
  required_providers {
    openstack = {
      source  = "terraform-provider-openstack/openstack"
      version = "~> 1.53.0"
    }
  }
}

provider "openstack" {
  user_name   = var.os_username
  password    = var.os_password
  auth_url    = var.os_auth_url
  tenant_name = var.os_project_name
  region      = var.os_region
 
}


variable "os_username" {}
variable "os_password" {}
variable "os_auth_url" {}
variable "os_project_name" {}
variable "os_region" {
  default = "RegionOne"
}

variable "ssh_key_name" {
  description = "Nom du keypair SSH à utiliser pour les VM"
  type        = string
}


data "openstack_compute_keypair_v2" "mykeypair" {
  name = var.ssh_key_name
}


resource "openstack_compute_instance_v2" "web1" {
  name            = "vmweb1"
  image_name      = "ubuntu24.04"
  flavor_name     = "moyenne"
  key_pair        = data.openstack_compute_keypair_v2.mykeypair.name
}

resource "openstack_compute_instance_v2" "db1" {
  name            = "vmdb1"
  image_name      = "ubuntu24.04"
  flavor_name     = "moyenne"
  key_pair        = data.openstack_compute_keypair_v2.mykeypair.name
}


output "web1_ip" {
  value = openstack_compute_instance_v2.web1.access_ip_v4
  description = "Adresse IP de la VM web1"
}


output "db1_ip" {
  value = openstack_compute_instance_v2.db1.access_ip_v4
  description = "Adresse IP de la VM db1"
}
