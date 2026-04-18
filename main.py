from src.engine import start_engine

def main():
    try:
        start_engine()
    except Exception as e:
        print(f"MAIN ERROR: {e}")

if __name__ == "__main__":
    main()