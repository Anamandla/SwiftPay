"""Master test runner — runs all SwiftPay tests"""
import sys, os, subprocess
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

files = [
    "tests/test_repositories.py",
    "tests/services/test_user_service.py",
    "tests/services/test_transaction_service.py",
    "tests/api/test_api.py",
]

total_pass = total_fail = 0
for f in files:
    print(f"\n{'='*55}\nRunning: {f}\n{'='*55}")
    result = subprocess.run([sys.executable, f], capture_output=True, text=True,
                            cwd=os.path.join(os.path.dirname(__file__), '..'))
    print(result.stdout)
    if result.stderr and "Error" in result.stderr:
        print("STDERR:", result.stderr[:500])
    # count from output
    for line in result.stdout.split('\n'):
        if 'Tests:' in line and 'passed' in line:
            parts = line.split()
            for i, p in enumerate(parts):
                if '/' in p:
                    nums = p.split('/')
                    total_pass += int(nums[0]); total_fail += int(nums[1]) - int(nums[0])

print(f"\n{'█'*55}")
print(f"TOTAL: {total_pass} passed, {total_fail} failed {'✅' if total_fail==0 else '❌'}")
print(f"{'█'*55}")
