Enabled easier submodule access

Allows::

    import sisl
    sisl.geom

and basically all variants. Using this mechanism the imports
are lazily done.

So now `import sisl.geom` is generally not required!
