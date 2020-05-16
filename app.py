#!/usr/bin/env python3

from aws_cdk import core

from star_base.star_base_stack import StarBaseStack


app = core.App()
StarBaseStack(app, "star-base")

app.synth()
