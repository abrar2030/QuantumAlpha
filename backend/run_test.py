"""
Simple test runner to verify backend starts
"""

import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

print("Testing backend startup...")
print("=" * 50)

try:
    print("1. Testing imports...")
    from main import QuantumAlphaApp

    print("   ✓ Main imports successful")

    print("\n2. Creating app instance...")
    app_instance = QuantumAlphaApp()
    print("   ✓ App instance created")

    print("\n3. Creating Flask app...")
    app = app_instance.create_app()
    print("   ✓ Flask app created")

    print("\n4. Checking app configuration...")
    print(f"   - Debug mode: {app.config.get('DEBUG', False)}")
    print(f"   - Secret key set: {bool(app.config.get('SECRET_KEY'))}")
    print(f"   - JWT key set: {bool(app.config.get('JWT_SECRET_KEY'))}")

    print("\n5. Checking routes...")
    routes = [str(rule) for rule in app.url_map.iter_rules()]
    print(f"   - Registered routes: {len(routes)}")
    print(f"   - Sample routes: {routes[:5]}")

    print("\n" + "=" * 50)
    print("✓ Backend is READY TO START!")
    print("=" * 50)
    print("\nTo run the backend:")
    print("  python3 main.py")
    print("  or")
    print("  gunicorn -w 4 -b 0.0.0.0:5000 'main:QuantumAlphaApp().create_app()'")

except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)
