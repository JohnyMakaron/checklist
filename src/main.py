try:
    from .application import ChecklistApplication
except ImportError:
    from application import ChecklistApplication


def main():
    app = ChecklistApplication()
    app.run()


if __name__ == "__main__":
    main()
