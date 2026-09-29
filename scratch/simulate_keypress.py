import sys

# Let's simulate the exact JS logic from page.tsx:

targetRomaji = "kousatennomannakaisoguhitonimagirete"
print(f"targetRomaji length: {len(targetRomaji)}")

# Check targetRomaji at index 16, 17, 18
for idx in range(15, 20):
    print(f"index {idx}: '{targetRomaji[idx]}'")

currentCharIndex = 17
currentPos = currentCharIndex

# Auto-skip non-alphanumeric
import re
while currentPos < len(targetRomaji) and not re.match(r'[a-z0-9]', targetRomaji[currentPos], re.I):
    currentPos += 1

print(f"currentPos: {currentPos}")
if currentPos >= len(targetRomaji):
    print("Already at end!")

remaining = targetRomaji[currentPos:]
expectedChar = remaining[0]
print(f"remaining: '{remaining}'")
print(f"expectedChar: '{expectedChar}'")

# Now let's test if user pressed 'i':
pressedChar = 'i'
matchedLength = 0

if pressedChar == expectedChar:
    matchedLength = 1

print(f"pressedChar '{pressedChar}' -> matchedLength: {matchedLength}")
