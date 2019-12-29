Role Name
=========

This role allows you to use Terraform variables (tfvars) as Ansible local facts.
It will convert the HCL tfvars to facts in JSON, uload the facts to the servers  
and optionally in the same play reload the Ansible setup module.  

Variables can be used in Ansible by following syntax `{{ ansible_local['tfvars']['my_variable'] }}`.  

**Note:**
Since the Ansible variable names can not contain the dash sign, it will be replaced by underscore.  
For example `my-var-1` by `my_var_1`.  

Role Variables
--------------

# Path to Ansible local facts
`local_facts_path: /etc/ansible/facts.d`

# Local facts file name. If changed for example to "different_file.facts",
# also the key will be {{ ansible_local['different_file']['some_variable'] }}
`local_facts_file: tfvars.fact`

# Enable if used with DT Pan-Net ALiEn (Application Lifecycle Engine)
`ALiEn: false`

# Path to Terraform variables file
# (ommited if variable ALiEn is true)
`tfvars_path: files`

# Terraform variables file name
`tfvars_file: vars.tfvars`

# Reload the Ansible facts after local facts are created
`reload_facts: false`

Example Playbook
----------------

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

License
-------

MIT
