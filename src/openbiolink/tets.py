import click



@click.group()
def main():
    pass


@main.group()
def embedded():
    pass


@main.group()
def symbolic():
    pass

@embedded.command()
def printo():
    print("embedded")

@symbolic.command()
def printo():
    print("symbolic")

if __name__ == "__main__":
    main()