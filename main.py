from fastapi import FastAPI

app = FastAPI(title="My API Docs")

@app.get("/")
def root():
    return {"message": "API is running!"}
def main():
    print("Hello from backend!")


if __name__ == "__main__":
    main()
