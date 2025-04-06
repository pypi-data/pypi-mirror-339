# LangGate Transform

Parameter transformation utilities for LangGate AI Gateway.

This package provides the core parameter transformation logic used by both:
- Local registry clients to transform parameters for direct model calls
- The Envoy external processor to transform parameters in the proxy

It implements a declarative approach to parameter transformation that can be:
1. Used directly in Python applications
2. Potentially reimplemented in other languages (like Go) for external processors
3. Extended with custom transformation rules
