import utils

class WeakRNG:
    """ Simple class for weak RNG """

    def __init__(self):
        self.rstate = 0
        self.maxn = 255
        self.a = 0  # Set this to correct value
        self.b = 0  # Set this to correct value
        self.p = 257
 
    def init_state(self, rstate):
        """ Initialise rstate """
        self.rstate = rstate # Set this to some value
        self.update_state()
 
    def update_state(self):
        """ Update state """
        self.rstate = (self.a * self.rstate + self.b) % self.p
 
    def get_prg_byte(self):
        """ Return a new PRG byte and update PRG state """
        b = self.rstate & 0xFF
        self.update_state()
        return b

# Initialise weak rng
wr = WeakRNG()
wr.init_state(0)

# Print ciphertext
CH = 'a432109f58ff6a0f2e6cb280526708baece6680acc1f5fcdb9523129434ae9f6ae9edc2f224b73a8'
print("Full ciphertext in hexa:", CH)

# Print known plaintext
pknown = 'Let all creation'
nb = len(pknown)
print("Known plaintext:", pknown)
pkh = utils.str_2_hex(pknown)
print("Plaintext in hexa:", pkh)

# Obtain first nb bytes of RNG
gh = utils.hexxor(pkh, CH[0:nb*2])
print("gh: " + gh)
gbytes = []
for i in range(nb):
    gbytes.append(ord(utils.hex_2_str(gh[2*i:2*i+2])))
print("Bytes of RNG: ")
print(gbytes)

# Break the LCG here:
# TODO 1: Find a and b, and set them in the RNG
for a in range (257):
  for b in range(257):

      found = True
      for i in range(1, len(gbytes)):
        if gbytes[i] != (a*gbytes[i-1] + b) % wr.p:
          found = False
          break
      if found:
          break
  if found:
    break

wr.a = a
wr.b = b
wr.init_state(gbytes[-1])

# TODO 2: Predict/generate rest of RNG bytes

for i in range((len(CH)-len(gh)//2)):
  gbytes.append(wr.get_prg_byte())

# TODO 3: Decrypt plaintext

key = "".join(utils.str_2_hex(chr(b) for b in gbytes))

# TODO 4: Print the full plaintext

plaintext = utils.hex_2_str(utils.hexxor(key, CH))
print("Full plaintext is:", plaintext)