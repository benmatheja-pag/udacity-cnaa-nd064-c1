# nd064_C1

## Cloud Native Fundamentals Scholarship Program Nanodegree Program - Solution from Ben

**Course Homepage**: https://sites.google.com/udacity.com/suse-cloud-native-foundations/home

**Instructor**: https://github.com/kgamanji

## Tips & Tricks

### Python App

Create virtual environment

````python
python3 -m venv venv
````

Source the virtual environment

````python
source venv/bin/activate
````

Install Pip Requirements

````python
pip install -r requirements.txt
````

Init the DB

````python
python init_db.py
````

### Helm and K8s

Lint a Template and check kube conformance

````bash
helm template ./ -f Values-Prod.yaml | kubeconform -strict   
````
