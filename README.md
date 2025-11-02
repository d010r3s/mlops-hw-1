```
docker build -t mlops-hw-1 .

docker run --rm `
  -v "${PWD}\input:/app/input" `
  -v "${PWD}\output:/app/output" `
  mlops-hw-1
```
