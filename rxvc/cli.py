"""Commands for controlling a Yamaha RX-V series receiver."""
import click
# Not spelling this correctly on purpose... needs fixed upstream.
from rxv.exceptions import ReponseException

import rxvc.cache as cache

CTX_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(invoke_without_command=True,
             no_args_is_help=True,
             context_settings=CTX_SETTINGS)
@click.option('--clear',
              is_flag=True,
              default=False,
              help="Clear the cache and look for receivers again.")
@click.pass_context
def cli(ctx, clear):
    """Control your Yamaha receiver from the command line, really fast.

    Taking advantage of caching (which can be cleared buy running rxvc
    with no command but with --clear), after the first run it's super
    fast. This cache is stored in ~/.rxvc_cache.

    Have fun!

    """
    if clear:
        print("Clearing receiver cache as requested...")
        cache.clear()

    receiver = cache.cached_receiver()
    if receiver is None:
        receiver = cache.find_receiver()
        cache.cache_receiver(receiver)

    ctx.obj = {}
    ctx.obj['avr'] = receiver


@cli.command(context_settings=CTX_SETTINGS)
@click.pass_context
def status(ctx):
    """Print overall status of the receiver."""
    status = ctx.obj['avr'].basic_status
    print(("\nPower: {on}\n"
           "Input: {input}\n"
           "Volume: {volume}\n"
           "Muted: {muted}\n").format(
               on=status.on,
               input=status.input,
               volume=status.volume,
               muted=status.mute))


@cli.command(context_settings=CTX_SETTINGS)
@click.pass_context
def inputs(ctx):
    """List valid input names for this receiver.

    These are names that can also be passed to the input command
    when using it to set an input.

    """
    print("Valid input names for this receiver are:")
    for input in ctx.obj['avr'].inputs():
        print('* ', input)


@cli.command(context_settings=CTX_SETTINGS)
@click.argument("input", nargs=-1)
@click.pass_context
def input(ctx, input):
    """See the current receiver input or set it if passed an
    argument that is a valid input for the receiver. Note that
    if it has spaces in it, you should wrap the whole argument
    in quotes space excaping and stuff.

    """
    avr = ctx.obj['avr']
    if input:
        if input[0] in avr.inputs():
            print("Setting receiver input to {}".format(input[0]))
            avr.input = input[0]
        else:
            print(("That's not a valid input. Run `rxvc inputs' to"
                   "get a list of them."))
    else:
        print("Current input is", avr.input)


# This command a little inconsistent with the input command in that
# setting the volume requires you pass an option rather than an
# argument. This is a limitation imposed by click. While with an
# option with the float type we can pass a negative number in,
# if we do this with an argument it tries to parse it as an option.
@cli.command(context_settings=CTX_SETTINGS)
@click.option('-v', '--vol', type=click.FLOAT, required=False)
@click.pass_context
def volume(ctx, vol):
    """Show the current receiver volume level, or set it with the
    -v/--vol option.

    """
    avr = ctx.obj['avr']
    if vol:
        try:
            avr.volume = vol
            click.echo(avr.volume)
        except ReponseException as e:
            if "Volume" in str(e):
                msg = "Volume must be specified in -0.5 increments."
                err = click.style(msg, fg='red')
                click.echo(err, err=True)
    else:
        click.echo(avr.volume)
