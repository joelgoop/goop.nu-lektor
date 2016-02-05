# -*- mode: ruby -*-
# vi: set ft=ruby :
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.provider "virtualbox" do |v|
    v.memory = 1024
  end
  config.vm.box = "ubuntu/trusty32"
  config.vm.network "forwarded_port", guest: 5000, host: 5000

  config.vm.synced_folder "src/", "/home/vagrant/src/"
  config.vm.provision "shell", inline: "sudo apt-get install -y python-pip python-dev && sudo pip install ansible==1.9.2 && sudo cp /usr/local/bin/ansible /usr/bin/ansible"
  config.vm.provision "ansible_local", version: "1.9.2", playbook: "provision/playbook.yml"
end