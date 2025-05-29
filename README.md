### How to run project

1. Clone repo:
  ```bash
  git clone https://github.com/AlexeyTarasov77/sca-backend 
  ```

3. Copy .env:
  ```bash
  cp .env.dev .env
  ```

3. Build and run compose services:
  ```bash
  make docker/build
  ```

4. Run migrations:
  ```bash
  make docker/run-migrations
  ```


### Postman collection to test endpoints:
**https://www.postman.com/co3n/my-workspace/request/6zs2358/add-target-note?tab=body**
