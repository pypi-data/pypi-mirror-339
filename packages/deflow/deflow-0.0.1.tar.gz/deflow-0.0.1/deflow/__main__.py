import typer

main = typer.Typer()


@main.command()
def hello(name: str):
    print(f"Hello {name}")


if __name__ == "__main__":
    main()
