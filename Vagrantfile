# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
    # The most common configuration options are documented and commented below.
    # For a complete reference, please see the online documentation at
    # https://docs.vagrantup.com.
  
    # Every Vagrant development environment requires a box. You can search for
    # boxes at https://vagrantcloud.com/search.
# 设置通用的镜像名，建议换成 41
  BOX_NAME = "generic/fedora39"
  config.ssh.username = "vagrant"
  config.ssh.password = "vagrant"
  config.ssh.insert_key = false  # 关键：不让 Vagrant 替换掉默认钥匙
  config.vm.define :client do |client|
    client.vm.box = BOX_NAME
    client.vm.box_version = ">= 0"  # 解除锁定，自动下载最新可用版本
    client.vm.network :private_network, ip: "192.168.56.100", netmask: "24"
    client.vm.network :private_network, ip: "192.168.57.100", netmask: "24"
    client.vm.network :private_network, ip: "192.168.58.100", netmask: "24"
    client.vm.hostname = "client"
    client.vm.provision "shell", path: "./scripts/init.sh"
  end

  config.vm.define :server do |server|
    server.vm.box = BOX_NAME
    server.vm.box_version = ">= 0"  # 这里之前是 39.20231031.1，现已修复
    server.vm.network :private_network, ip: "192.168.56.101", netmask: "24"
    server.vm.network :private_network, ip: "192.168.57.101", netmask: "24"
    server.vm.network :private_network, ip: "192.168.58.101", netmask: "24"
    server.vm.hostname = "server"
    server.vm.provision "shell", path: "./scripts/init.sh"
  end
  
    # Disable automatic box update checking. If you disable this, then
    # boxes will only be checked for updates when the user runs
    # `vagrant box outdated`. This is not recommended.
    # config.vm.box_check_update = false
  
    # Create a forwarded port mapping which allows access to a specific port
    # within the machine from a port on the host machine. In the example below,
    # accessing "localhost:8080" will access port 80 on the guest machine.
    # NOTE: This will enable public access to the opened port
    # config.vm.network "forwarded_port", guest: 80, host: 8080
  
    # Create a forwarded port mapping which allows access to a specific port
    # within the machine from a port on the host machine and only allow access
    # via 127.0.0.1 to disable public access
    # config.vm.network "forwarded_port", guest: 80, host: 8080, host_ip: "127.0.0.1"
  
    # Create a private network, which allows host-only access to the machine
    # using a specific IP.
    # config.vm.network "private_network", ip: "192.168.33.10"
  
    # Create a public network, which generally matched to bridged network.
    # Bridged networks make the machine appear as another physical device on
    # your network.
    # config.vm.network "public_network"
  
    # Share an additional folder to the guest VM. The first argument is
    # the path on the host to the actual folder. The second argument is
    # the path on the guest to mount the folder. And the optional third
    # argument is a set of non-required options.
    # config.vm.synced_folder "../data", "/vagrant_data"
  
    # Disable the default share of the current code directory. Doing this
    # provides improved isolation between the vagrant box and your host
    # by making sure your Vagrantfile isn't accessible to the vagrant box.
    # If you use this you may want to enable additional shared subfolders as
    # shown above.
    # config.vm.synced_folder ".", "/vagrant", disabled: true
  
    # Provider-specific configuration so you can fine-tune various
    # backing providers for Vagrant. These expose provider-specific options.
    # Example for VirtualBox:
    #
    config.vm.provider "virtualbox" do |vb|
        vb.memory = 2048
        vb.cpus = 2
    end
    #
    # View the documentation for the provider you are using for more
    # information on available options.
  
    # Enable provisioning with a shell script. Additional provisioners such as
    # Ansible, Chef, Docker, Puppet and Salt are also available. Please see the
    # documentation for more information about their specific syntax and use.
    # config.vm.provision "shell", inline: <<-SHELL
    #   apt-get update
    #   apt-get install -y apache2
    # SHELL
  end