
#!/usr/bin/env python

import sys

# Simulate an invalid test with a syntax error
print 'Hello, world!' # This is a syntax error in Python 3
sys.exit(1) # This line will not be reached if syntax error occurs
