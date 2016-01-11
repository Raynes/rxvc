"""Commands for controlling a Yamaha RX-V series receiver."""
import sys
import click
import rxv

import rxvc.cache as cache

CTX_SETTINGS = dict(help_option_names=['-h', '--help'])


def find_receiver():
    """Look for a receiver using rxv's find method. If no receiver
    is found, print an appropriate error, otherwise return the first
    (if multiple are found) receiver

    """
    receiver = None
    print("Looking for receivers...")
    found_receivers = rxv.find()
    if len(found_receivers) > 1:
        print("Found multiple receivers, choosing the first one.")
        receiver = found_receivers[0]
        print("Using {}".format(receiver.friendly_name))
    elif not found_receivers:
        print("No reciever found, giving up.")
        sys.exit(1)
    else:
        receiver = found_receivers[0]
        print("Found receiver:", receiver.friendly_name)

    return receiver


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
        receiver = find_receiver()
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
