tfvars2facts
=========
<div class="row">
 <img src="https://github.com/MonolithProjects/ansible-tfvars2facts/raw/media/logo_rectangle.png" width="13%" height="13%" alt="Logo" align="right"/>

<a href="https://github.com/MonolithProjects/ansible-tfvars2facts/actions"><img src="https://github.com/MonolithProjects/ansible-tfvars2facts/workflows/molecule%20test/badge.svg?branch=master"/></a>
<img src="https://img.shields.io/ansible/quality/45539?style=flat&logo=ansible"/>
<img src="https://img.shields.io/ansible/role/d/45539"/><br>
<img src="https://img.shields.io/github/v/release/MonolithProjects/ansible-tfvars2facts"/>
</div>

This role allows you to use Terraform variables (tfvars) as Ansible local facts.
It will convert the HCL tfvars to facts in JSON format and upload them to the servers.
Optionally the Ansible facts can be reloaded during the same play.  

Variables can be used in Ansible by following syntax `{{ ansible_local['tfvars']['my_variable'] }}`.  

**Note:**
Since the Ansible variable names can not contain the dash sign, the dash sign(s) will be replaced by underscore.  
For example `my-var-1` will be `my_var_1`.  

Role Variables
--------------
```
# Path to Ansible local facts  
local_facts_path: /etc/ansible/facts.d

# Local facts file name. If changed for example to "different_file.facts",
# also the key will be {{ ansible_local['different_file']['some_variable'] }}  
local_facts_file: tfvars.fact

# Enable if used with DT Pan-Net ALiEn (Application Life-cycle Engine)  
ALiEn: false

# Path to Terraform variables file (ommited if variable ALiEn is true)  
tfvars_path: files

# Terraform variables file name  
tfvars_file: vars.tfvars

# Reload the Ansible facts after local facts are created  
reload_facts: false
```

Example Playbook
----------------

Basic playbook.
```
---
- name: Example
  hosts: all
  become: yes
  roles:
    - role: ansible-tfvars2facts
```

Playbook with post task which is using the variable taken during role run
(for this the facts needs to be reloaded during the role run).
```
---
- name: Example
  hosts: all
  become: yes
  vars:
    reload_facts: true
  roles:
    - role: ansible-tfvars2facts
  post_tasks:
    - name: Test a variable
      debug:
        msg: "Value of the test variable is {{ ansible_local['tfvars']['test_var'] }}"
```

License
-------

MIT
