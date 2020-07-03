# Please specify the operating system you want to deploy on your VM:
os_jumphost_template            = "RedHat Linux 7"
os_app_template                 = "RedHat Linux 7"

#Please specify the name of your VMs:
vm_name                = ["genDMZLB-1", "genDMZLB_-2"]

# Please specify the name of the folder where the VM should be placed within the hosts and templates view of the vCenter:
folder                 = "LinuX-LBs"

## Please specify the characteristics of your VM:
vm_count               = "2"
memory                 = "1024" #hoho comment
vip-address-frontend    = ["192.168.192.20", "192.168.192.21"]
vip-ad-d-r-e-s_s-backend-x_y    = "192.168.67.1"