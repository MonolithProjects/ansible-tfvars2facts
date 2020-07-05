# GitHub Actions Runner

[![Galaxy Quality](https://img.shields.io/ansible/quality/45539?style=flat&logo=ansible)](https://galaxy.ansible.com/monolithprojects/tfvars2facts)
[![Role version](https://img.shields.io/github/v/release/MonolithProjects/ansible-tfvars2facts)](https://galaxy.ansible.com/monolithprojects/tfvars2facts)
[![Role downloads](https://img.shields.io/ansible/role/d/45539)](https://galaxy.ansible.com/monolithprojects/tfvars2facts)
[![GitHub Actions](https://github.com/MonolithProjects/ansible-tfvars2facts/workflows/molecule%20test/badge.svg?branch=master)](https://github.com/MonolithProjects/ansible-tfvars2facts/actions)
[![License](https://img.shields.io/github/license/MonolithProjects/ansible-tfvars2facts)](https://github.com/MonolithProjects/ansible-tfvars2facts/blob/master/LICENSE)

This Ansible module translates the Terraform tfvrs file to Ansible Local Facts.
You can run this module on the remote hosts or run it locally once and copy the output JSON file to /etc/ansib.e/facts.d/ directory on the remote host.  

Variables can be used in Ansible by following syntax `{{ ansible_local['tfvars']['my_variable'] }}`.  

**Note:**
Since the Ansible variable names can not contain the dash sign, the dash sign(s) will be replaced by underscore.  
For example `my-var-1` will be `my_var_1`.

## Requirements

* Ansible 2.8+

* Role must run in privileged mode (`become: yes`)

## Role Variables

This is a copy from `defaults/main.yml`

```yaml
# Path to Ansible local facts
local_facts_path: /etc/ansible/facts.d

# Local facts file name. If changed for example to "different_file.facts",
# also the key will be {{ ansible_local['different_file']['some_variable'] }}
local_facts_file: tfvars.fact

# Enable if used with DT Pan-Net ALiEn (Application Lifecycle Engine)
ALiEn: false

# Path to Terraform variables file
# (ommited if variable ALiEn is true)
tfvars_path: files

# Terraform variables file name
tfvars_file: vars.tfvars

# Reload the Ansible facts after local facts are created
reload_facts: false
```

## Example Playbook

In this example the role will translate Terraform variables in `files/vars.tfvars` and will upload it as an Ansible facts file to the remote hosts.
The role will also reload the Ansible Facts, so the new facts will be ready for the next role/post_task.

```yaml
---
- name: Simple Example
  hosts: all
  become: yes
  vars:
    reload_facts: yes
  roles:
    - role: ansible-tfvars2facts
```

## License

MIT

## Author Information

Created in 2020 by Michal Muransky/DT Pan-Net
