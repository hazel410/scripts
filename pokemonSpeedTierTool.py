import sys

BUILD_DESCS = [" -0 ", "  0 ", " +0 " , "-255", " 255", "+255"]

class PKMN:
  def __init__(self, baseSpeed, mult):
    self.mult = mult
    self.baseSpeed = baseSpeed
    self.allSpeeds = []

    for evs in [0, 252]:
      for nature in [0.9, 1.0, 1.1]:
        self.allSpeeds.append(self.calcSpeed(nature, evs))
    
    self.speedIndex = 0
    self.currentSpeed = self.allSpeeds[self.speedIndex]
    self.currentBuild = BUILD_DESCS[self.speedIndex]

  def calcSpeed(self, nature, evs):
    return (((2 * self.baseSpeed + 31 + (evs // 4) + 5) * nature) * self.mult) // 1
  
  def incrSpeed(self):
    if self.speedIndex < 5:
      self.speedIndex += 1
      self.currentSpeed = self.allSpeeds[self.speedIndex]
      self.currentBuild = BUILD_DESCS[self.speedIndex]
      return True
    else:
      return False

class PKMNMANAGER:
  # not bothering in generalizing for n pkmn
  def __init__(self, args):
    self.pkmn1 = PKMN(int(args[0]), float(args[1]))
    self.pkmn2 = PKMN(int(args[2]), float(args[3]))
    self.wins = [] # pkmn 1's perspective
  
  def speedWar(self):
    output = []
    while self.pkmn1.speedIndex * self.pkmn2.speedIndex <= 25:
      if self.pkmn1.currentSpeed > self.pkmn2.currentSpeed:
        output.append("WIN! --- (" + self.pkmn1.currentBuild + ") > (" + self.pkmn2.currentBuild + ")")
        incrSuccess = self.pkmn2.incrSpeed()
      elif self.pkmn1.currentSpeed < self.pkmn2.currentSpeed:
        output.append("LOS! --- (" + self.pkmn1.currentBuild + ") < (" + self.pkmn2.currentBuild + ")")
        incrSuccess = self.pkmn1.incrSpeed()
      else:
        output.append("TIE! --- (" + self.pkmn1.currentBuild + ") = (" + self.pkmn2.currentBuild + ")")
        incrSuccess = self.pkmn1.incrSpeed() & self.pkmn2.incrSpeed()
      if not incrSuccess:
        break
    output.reverse()
    for line in output:
      print(line)

def main(args):
  mngr = PKMNMANAGER(args)
  mngr.speedWar()

if __name__ == "__main__":
  main(sys.argv[1:])