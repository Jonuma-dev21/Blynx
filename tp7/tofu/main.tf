
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
  description = "Nom du keypair SSH pour les VM"
  type        = string
}

variable "cluster_name" {
  description = "Nom du cluster"
  type        = string
  default     = "tp7-cluster"
}




data "openstack_compute_keypair_v2" "mykeypair" {
  name = var.ssh_key_name
}


resource "openstack_compute_instance_v2" "cluster_vm1" {
  name        = "cluster_vm1"
  image_name  = "debian13"
  flavor_name = "tres puissante"
  key_pair    = data.openstack_compute_keypair_v2.mykeypair.name

  metadata = {
    Cluster = var.cluster_name
    Role    = "control_plane"
    Env     = "dev"
  }
}

resource "openstack_compute_instance_v2" "cluster_vm2" {
  name            = "cluster_vm2"
  image_name      = "debian13"
  flavor_name     = "moyenne"
  key_pair        = data.openstack_compute_keypair_v2.mykeypair.name

metadata = {

  Cluster = var.cluster_name
    Role    = "noeud"
    Env     = "dev"
  }

}
resource "openstack_compute_instance_v2" "cluster_vm3" {
  name            = "cluster_vm3"
  image_name      = "debian13"
  flavor_name     = "moyenne"
  key_pair        = data.openstack_compute_keypair_v2.mykeypair.name

metadata = {
  Cluster = var.cluster_name
    Role    = "noeud"
    Env     = "dev"
  }

}

output "cluster_vm1" {
  value = openstack_compute_instance_v2.cluster_vm1.access_ip_v4
  description = "Adresse IP de la VM cluster_vm1"
}

output "cluster_vm2" {
  value = openstack_compute_instance_v2.cluster_vm2.access_ip_v4
  description = "Adresse IP de la VM cluster_vm2"
}

output "cluster_vm3" {
  value = openstack_compute_instance_v2.cluster_vm3.access_ip_v4
  description = "Adresse IP de la VM cluster_vm3"
}

