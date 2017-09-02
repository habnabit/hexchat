#!/usr/bin/env python3

import sys
import cffi

with open(sys.argv[1]) as f:
    data = f.read()

builder = cffi.FFI()
builder.embedding_api(data)

builder.set_source('hexchat', '''
#undef HAVE_STRINGS_H
#undef HAVE_MEMRCHR

#include "config.h"
#include "hexchat-plugin.h"

static char *NAME = "python";
static char *VERSION = "1.0";
static hexchat_plugin *ph;

static int on_pytest(char **, char **, void *);

int
hexchat_plugin_init(hexchat_plugin *plugin_handle,
                    char **plugin_name,
                    char **plugin_desc,
                    char **plugin_version,
                    char *arg)
{
    ph = plugin_handle;
    *plugin_name = NAME;
    *plugin_version = VERSION;
    *plugin_desc = "FOoo";

    hexchat_hook_command(ph, "pytest", HEXCHAT_PRI_NORM, on_pytest, NULL, NULL);

    return 1;
}

int
hexchat_plugin_deinit(void)
{
    return 1;
}
''')

builder.embedding_init_code("""
    from hexchat import ffi, lib
    import hexchat

    @ffi.def_extern()
    def on_pytest(word, word_eol, userdata):
        help(ffi)
        help(lib)
        for i in range(1, 32, 1):
            string = ffi.string(word[i])
            if string == b'':
                break
            print(string.decode())
        return 0
""")

builder.emit_c_code(sys.argv[2])
