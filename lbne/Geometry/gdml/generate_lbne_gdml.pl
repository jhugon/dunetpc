#!/usr/bin/perl

use Math::Trig;
use XML::LibXML;
use Getopt::Long;

$outfile					=	"lbne.gdml";
$nCryos						= 2;		# can get rid of this later, 1 corresponds to 1st gdml iteration

#Specific H,W,L of LBNE
$CryostatWidth		=	2400;
$CryostatHeight		=	1500;
$CryostatLength		=	4500;

#detector variables
$SteelThickness		=	0.5*2.54;
$ArgonWidth				=	$CryostatWidth-2*$SteelThickness;
$ArgonHeight			=	$CryostatHeight-2*$SteelThickness;
$ArgonLength			=	$CryostatLength-2*$SteelThickness;

#set rock thickness
#  1000 for normal 10m thickness
#  10000 for lbnebulky
$RockThickness		=	1000;

$ConcretePadding	=	50;
$GlassFoamPadding	=	100;
$TotalPadding			=	$ConcretePadding+$GlassFoamPadding+$SteelThickness;
$CavernWidth			=	$ArgonWidth+2*$TotalPadding;
$CavernHeight			=	$ArgonHeight+$TotalPadding;
$CavernLength			=	$nCryos*$CryostatLength+($nCryos+1)*$TotalPadding;

$FiducialWidth		=	$CryostatWidth-100;
$FiducialHeight		=	$CryostatHeight-100;
$FiducialLength		=	$CryostatLength-100;

$TPCWidth					=	$FiducialWidth/2;
$TPCHeight				=	$FiducialHeight/2;
$TPCLength				=	$FiducialLength;

$TPCWireThickness=0.015;
$TPC_WireSpacing=0.3;

$Pi=3.14159;

gen_header();
gen_materials();
gen_lbne();
exit;






sub gen_lbne()
{
  # Set up the output file.
  $LBNE = ">>" . $outfile;
  open(LBNE) or die("Could not open file $LBNE for writing");

  print LBNE <<EOF;
 <solids>
    <box name="World" lunit="cm" 
      x="$CryostatWidth+2*($RockThickness+$TotalPadding)+$TPCWidth" 
      y="$CryostatHeight+2*($RockThickness+$TotalPadding)" 
      z="$CavernLength+2*$RockThickness+$TPCLength"/>
    <box name="LowerRock" lunit="cm" 
      x="$CryostatWidth+2*($RockThickness+$TotalPadding)" 
      y="$CryostatHeight+$RockThickness+$TotalPadding" 
      z="$CavernLength+2*$RockThickness"/>
    <box name="RockBottom" lunit="cm" 
      x="$CryostatWidth+2*$TotalPadding" 
      y="$RockThickness" 
      z="$CavernLength"/>
    <box name="LowerCavern" lunit="cm" 
      x="$CryostatWidth+2*$TotalPadding"
      y="$CryostatHeight+$RockThickness+$TotalPadding+2"
      z="$CavernLength"/>
    <subtraction name="LowerRockWithCavern">
      <first ref="LowerRock"/>
      <second ref="LowerCavern"/>
    </subtraction>
    <box name="UpperRock" lunit="cm" 
      x="$CryostatWidth+2*($RockThickness+$TotalPadding)" 
      y="$RockThickness" 
      z="$CavernLength+2*$RockThickness"/>
    <box name="UpperCavern" lunit="cm" 
      x="$CryostatWidth+2*$TotalPadding+1000"
      y="$RockThickness+20"
      z="$CavernLength+1000"/>
    <box name="RockTop" lunit="cm" 
      x="$CryostatWidth+2*$TotalPadding+1000" 
      y="$RockThickness-500" 
      z="$CavernLength+1000"/>
    <subtraction name="UpperRockWithCavern">
      <first ref="UpperRock"/>
      <second ref="UpperCavern"/>
    </subtraction>
    <box name="DetEnclosure" lunit="cm" 
      x="$CryostatWidth+2*$TotalPadding"
      y="$CryostatHeight+2*$TotalPadding"
      z="$CavernLength"/>
    <box name="ConcreteCylinder" lunit="cm" 
      x="$CryostatWidth+2*$TotalPadding"
      y="$CryostatHeight+$TotalPadding"
      z="$CavernLength"/>
    <box name="ConcreteBottom" lunit="cm" 
      x="$CryostatWidth+2*($TotalPadding-$ConcretePadding)"
      y="$ConcretePadding"
      z="$CavernLength-2*$ConcretePadding"/>
    <box name="ConcreteCavern" lunit="cm" 
      x="$CryostatWidth+2*($TotalPadding-$ConcretePadding)"
      y="$CryostatHeight+$TotalPadding+2"
      z="$CavernLength-2*$ConcretePadding"/>
    <subtraction name="ConcreteWithCavern">
      <first ref="ConcreteCylinder"/>
      <second ref="ConcreteCavern"/>
    </subtraction>
    <box name="Cryostat" lunit="cm" 
      x="$CryostatWidth" 
      y="$CryostatHeight" 
      z="$CryostatLength"/>
    <box name="ArgonInterior" lunit="cm" 
      x="$ArgonWidth"
      y="$ArgonHeight"
      z="$ArgonLength"/>
    <subtraction name="SteelShell">
      <first ref="Cryostat"/>
      <second ref="ArgonInterior"/>
    </subtraction>
    <box name="TPC" lunit="cm" 
      x="$TPCWidth" 
      y="$TPCHeight" 
      z="$TPCLength"/>
    <box name="TPCPlane" lunit="cm" 
      x="0.1" 
      y="0.9*$TPCHeight" 
      z="0.9*$TPCLength"/>
    <tube name="TPCWire"
      rmax="0.5*$TPCWireThickness"
      z="0.89*$TPCHeight"               
      deltaphi="2*$Pi"
      aunit="rad"
      lunit="cm"/>
    <box name="Cathode" lunit="cm"
      x="1"
      y="$TPCHeight"
      z="$TPCLength"/>
  </solids>
  <structure>
    <volume name="volSteelShell">
      <materialref ref="STEEL_STAINLESS_Fe7Cr2Ni" />
      <solidref ref="SteelShell" />
    </volume>
    <volume name="volTPCWire">
      <materialref ref="STEEL_STAINLESS_Fe7Cr2Ni" />
      <solidref ref="TPCWire" />
    </volume>
    <volume name="volTPCPlane">
      <materialref ref="LAr"/>
      <solidref ref="TPCPlane"/>
EOF

    $count=1;
    for ( $i=-0.3*$TPCLength ; $i < 0.3*$TPCLength ; $i+=$TPC_WireSpacing ) {
      $wire_zpos=$i;
      print LBNE <<EOF;
      <physvol>
        <volumeref ref="volTPCWire"/>
        <position name="posTPCWire$count" unit="cm" x="0" y="0" z="$wire_zpos"/>
        <rotation name="rTPCWire$count" unit="deg" x="60" y="0" z="0"/>
      </physvol>
EOF
      $count++;
    }
    print LBNE <<EOF;
    </volume>
    <volume name="volCathode">
      <materialref ref="STEEL_STAINLESS_Fe7Cr2Ni" />
      <solidref ref="Cathode" />
    </volume>
    <volume name="volTPC">
      <materialref ref="LAr" />
      <solidref ref="TPC" />
      <physvol>
        <volumeref ref="volTPCPlane"/>
        <position name="posTPCPlane1" unit="cm" x="(-$TPCWidth/2)+0.051+0.3" y="0" z="0"/>
      </physvol>
      <physvol>
        <volumeref ref="volTPCPlane"/>
        <position name="posTPCPlane2" unit="cm" x="(-$TPCWidth/2)+0.051" y="0" z="0"/>
        <rotation name="rTPCPlane2" unit="deg" x="0" y="180" z="0"/>
      </physvol>
      <physvol>
        <volumeref ref="volCathode"/>
        <position name="posCathode" unit="cm" x="($TPCWidth/2)-0.5" y="0" z="0"/>
      </physvol>
    </volume>
    <volume name="volCryostat">
      <materialref ref="LAr" />
      <solidref ref="Cryostat" />
      <physvol>
        <volumeref ref="volSteelShell"/>
        <position name="posSteelShell" unit="cm" x="0" y="0" z="0"/>
      </physvol>
EOF

    $TPC_X=$TPCWidth/2  + 5;  # +5 is for padding
    $TPC_Y=$TPCHeight/2 + 5;  # +5 is for padding
    print LBNE <<EOF;
      <physvol>
        <volumeref ref="volTPC"/>
        <position name="posTPC1" unit="cm" x="$TPC_X" y="$TPC_Y" z="0"/>
      </physvol>
      <physvol>
        <volumeref ref="volTPC"/>
        <position name="posTPC2" unit="cm" x="$TPC_X" y="-$TPC_Y" z="0"/>
      </physvol>
      <physvol>
        <volumeref ref="volTPC"/>
        <position name="posTPC3" unit="cm" x="-$TPC_X" y="-$TPC_Y" z="0"/>
        <rotation name="rTPC3" unit="deg" x="0" y="180" z="0"/>
      </physvol>
      <physvol>
        <volumeref ref="volTPC"/>
        <position name="posTPC4" unit="cm" x="-$TPC_X" y="$TPC_Y" z="0"/>
        <rotation name="rTPC4" unit="deg" x="0" y="180" z="0"/>
      </physvol>
EOF
    print LBNE <<EOF;
    </volume>
    <volume name="volConcreteWithCavern">
      <materialref ref="Concrete"/>
      <solidref ref="ConcreteWithCavern"/>
    </volume>
    <volume name="volConcreteBottom">
      <materialref ref="Concrete"/>
      <solidref ref="ConcreteBottom"/>
    </volume>
    <volume name="volDetEnclosure">
      <materialref ref="Air"/>
      <solidref ref="DetEnclosure"/>
EOF

		if($nCryos==1){
		    print LBNE <<EOF;
      <physvol>
        <volumeref ref="volCryostat"/>
        <position name="posCryostat" unit="cm" x="0" y="0" z="0"/>
      </physvol>
EOF
		}elsif($nCryos==2){
				    print LBNE <<EOF;
      <physvol>
        <volumeref ref="volCryostat"/>
        <position name="posCryostat1" unit="cm" x="0" y="0" z="0.25*$CavernLength"/>
      </physvol>
      <physvol>
        <volumeref ref="volCryostat"/>
        <position name="posCryostat2" unit="cm" x="0" y="0" z="-0.25*$CavernLength"/>
      </physvol>
EOF
		}

    print LBNE <<EOF;

      <physvol>
        <volumeref ref="volConcreteWithCavern"/>
        <position name="posConcreteWithCavern" unit="cm" x="0" y="-0.5*($TotalPadding-$ConcretePadding)" z="0"/>
      </physvol>
      <physvol>
        <volumeref ref="volConcreteBottom"/>
        <position name="posConcreteBottom" unit="cm" x="0" y="-0.5*($CryostatHeight+$TotalPadding)" z="0"/>
      </physvol>
    </volume>
    <volume name="volLowerRockWithCavern">
      <materialref ref="DUSEL_Rock"/>
      <solidref ref="LowerRockWithCavern"/>
    </volume>
    <volume name="volRockTop">
      <materialref ref="DUSEL_Rock"/>
      <solidref ref="RockTop"/>
    </volume>
    <volume name="volUpperRockWithCavern">
      <materialref ref="DUSEL_Rock"/>
      <solidref ref="UpperRockWithCavern"/>
    </volume>
    <volume name="volRockBottom">
      <materialref ref="DUSEL_Rock"/>
      <solidref ref="RockBottom"/>
    </volume>
    <volume name="volWorld" >
      <materialref ref="Air"/>
      <solidref ref="World"/>
      <physvol>
        <volumeref ref="volDetEnclosure"/>
        <position name="posDetEnclosure" unit="cm" x="0.5*$TPCWidth" y="0" z="0.5*$TPCLength"/>
      </physvol>
      <physvol>
        <volumeref ref="volLowerRockWithCavern"/>
        <position name="posLowerRockWithCavern" unit="cm" x="0.5*$TPCWidth" y="-0.5*$RockThickness" z="0.5*$TPCLength"/>
      </physvol>
      <physvol>
        <volumeref ref="volRockBottom"/>
        <position name="posRockBottom" unit="cm" x="0.5*$TPCWidth" y="-0.5*($RockThickness+$CryostatHeight+$TotalPadding)" z="0.5*$TPCLength"/>
      </physvol>
      <physvol>
        <volumeref ref="volUpperRockWithCavern"/>
        <position name="posUpperRockWithCavern" unit="cm" x="0.5*$TPCWidth" y="0.5*($RockThickness+$CryostatHeight)" z="0.5*$TPCLength"/>
      </physvol>
      <physvol>
        <volumeref ref="volRockTop"/>
        <position name="posRockTop" unit="cm" x="0.5*$TPCWidth" y="0.5*($RockThickness-500+$CryostatHeight)+500" z="0.5*$TPCLength"/>
      </physvol>
    </volume>
  </structure>
  <setup name="Default" version="1.0">
    <world ref="volWorld" />
  </setup>
</gdml>
EOF
   close(LBNE);
}


#generates necessary gd/xml header
sub gen_header() 
{

  $LBNE = ">" . $outfile;
  open(LBNE) or die("Could not open file $LBNE for writing");
  print LBNE <<EOF;
<?xml version="1.0" encoding="UTF-8" ?>
<gdml xmlns:gdml="http://cern.ch/2001/Schemas/GDML"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:noNamespaceSchemaLocation="GDMLSchema/gdml.xsd">
EOF
}


sub gen_materials() 
{

  $LBNE = ">>" . $outfile;
  open(LBNE) or die("Could not open file $LBNE for writing");
  print LBNE <<EOF;
<materials>
  <element name="videRef" formula="VACUUM" Z="1">  <atom value="1"/> </element>
  <element name="bromine" formula="Br" Z="35"> <atom value="79.904"/> </element>
  <element name="hydrogen" formula="H" Z="1">  <atom value="1.0079"/> </element>
  <element name="nitrogen" formula="N" Z="7">  <atom value="14.0067"/> </element>
  <element name="oxygen" formula="O" Z="8">  <atom value="15.999"/> </element>
  <element name="aluminum" formula="Al" Z="13"> <atom value="26.9815"/>  </element>
  <element name="silicon" formula="Si" Z="14"> <atom value="28.0855"/>  </element>
  <element name="carbon" formula="C" Z="6">  <atom value="12.0107"/>  </element>
  <element name="potassium" formula="K" Z="19"> <atom value="39.0983"/>  </element>
  <element name="chromium" formula="Cr" Z="24"> <atom value="51.9961"/>  </element>
  <element name="iron" formula="Fe" Z="26"> <atom value="55.8450"/>  </element>
  <element name="nickel" formula="Ni" Z="28"> <atom value="58.6934"/>  </element>
  <element name="calcium" formula="Ca" Z="20"> <atom value="40.078"/>   </element>
  <element name="magnesium" formula="Mg" Z="12"> <atom value="24.305"/>   </element>
  <element name="sodium" formula="Na" Z="11"> <atom value="22.99"/>    </element>
  <element name="titanium" formula="Ti" Z="22"> <atom value="47.867"/>   </element>
  <element name="argon" formula="Ar" Z="18"> <atom value="39.9480"/>  </element>
  <element name="sulphur" formula="S" Z="16"> <atom value="32.065"/>  </element>
  <element name="phosphorus" formula="P" Z="16"> <atom value="30.973"/>  </element>

  <material name="Vacuum" formula="Vacuum">
   <D value="1.e-25" unit="g/cm3"/>
   <fraction n="1.0" ref="videRef"/>
  </material>

  <material name="ALUMINUM_Al" formula="ALUMINUM_Al">
   <D value="2.6990" unit="g/cm3"/>
   <fraction n="1.0000" ref="aluminum"/>
  </material>

  <material name="SILICON_Si" formula="SILICON_Si">
   <D value="2.3300" unit="g/cm3"/>
   <fraction n="1.0000" ref="silicon"/>
  </material>

  <material name="epoxy_resin" formula="C38H40O6Br4">
   <D value="1.1250" unit="g/cm3"/>
   <composite n="38" ref="carbon"/>
   <composite n="40" ref="hydrogen"/>
   <composite n="6" ref="oxygen"/>
   <composite n="4" ref="bromine"/>
  </material>

  <material name="SiO2" formula="SiO2">
   <D value="2.2" unit="g/cm3"/>
   <composite n="1" ref="silicon"/>
   <composite n="2" ref="oxygen"/>
  </material>

  <material name="Al2O3" formula="Al2O3">
   <D value="3.97" unit="g/cm3"/>
   <composite n="2" ref="aluminum"/>
   <composite n="3" ref="oxygen"/>
  </material>

  <material name="Fe2O3" formula="Fe2O3">
   <D value="5.24" unit="g/cm3"/>
   <composite n="2" ref="iron"/>
   <composite n="3" ref="oxygen"/>
  </material>

  <material name="CaO" formula="CaO">
   <D value="3.35" unit="g/cm3"/>
   <composite n="1" ref="calcium"/>
   <composite n="1" ref="oxygen"/>
  </material>

  <material name="MgO" formula="MgO">
   <D value="3.58" unit="g/cm3"/>
   <composite n="1" ref="magnesium"/>
   <composite n="1" ref="oxygen"/>
  </material>

  <material name="Na2O" formula="Na2O">
   <D value="2.27" unit="g/cm3"/>
   <composite n="2" ref="sodium"/>
   <composite n="1" ref="oxygen"/>
  </material>

  <material name="TiO2" formula="TiO2">
   <D value="4.23" unit="g/cm3"/>
   <composite n="1" ref="titanium"/>
   <composite n="2" ref="oxygen"/>
  </material>

  <material name="FeO" formula="FeO">
   <D value="5.745" unit="g/cm3"/>
   <composite n="1" ref="iron"/>
   <composite n="1" ref="oxygen"/>
  </material>

  <material name="CO2" formula="CO2">
   <D value="1.562" unit="g/cm3"/>
   <composite n="1" ref="iron"/>
   <composite n="2" ref="oxygen"/>
  </material>

  <material name="P2O5" formula="P2O5">
   <D value="1.562" unit="g/cm3"/>
   <composite n="2" ref="phosphorus"/>
   <composite n="5" ref="oxygen"/>
  </material>

  <material formula=" " name="DUSEL_Rock">
    <D value="2.82" unit="g/cc"/>
    <fraction n="0.5267" ref="SiO2"/>
    <fraction n="0.1174" ref="FeO"/>
    <fraction n="0.1025" ref="Al2O3"/>
    <fraction n="0.0473" ref="MgO"/>
    <fraction n="0.0422" ref="CO2"/>
    <fraction n="0.0382" ref="CaO"/>
    <fraction n="0.0240" ref="carbon"/>
    <fraction n="0.0186" ref="sulphur"/>
    <fraction n="0.0053" ref="Na2O"/>
    <fraction n="0.00070" ref="P2O5"/>
    <fraction n="0.0771" ref="oxygen"/>
  </material> 

  <material name="fibrous_glass">
   <D value="2.74351" unit="g/cm3"/>
   <fraction n="0.600" ref="SiO2"/>
   <fraction n="0.118" ref="Al2O3"/>
   <fraction n="0.001" ref="Fe2O3"/>
   <fraction n="0.224" ref="CaO"/>
   <fraction n="0.034" ref="MgO"/>
   <fraction n="0.010" ref="Na2O"/>
   <fraction n="0.013" ref="TiO2"/>
  </material>

  <material name="FR4">
   <D value="1.98281" unit="g/cm3"/>
   <fraction n="0.47" ref="epoxy_resin"/>
   <fraction n="0.53" ref="fibrous_glass"/>
  </material>

  <material name="STEEL_STAINLESS_Fe7Cr2Ni" formula="STEEL_STAINLESS_Fe7Cr2Ni">
   <D value="7.9300" unit="g/cm3"/>
   <fraction n="0.0010" ref="carbon"/>
   <fraction n="0.1792" ref="chromium"/>
   <fraction n="0.7298" ref="iron"/>
   <fraction n="0.0900" ref="nickel"/>
  </material>

  <material name="LAr" formula="LAr">
   <D value="1.40" unit="g/cm3"/>
   <fraction n="1.0000" ref="argon"/>
  </material>

  <material formula=" " name="Air">
   <D value="0.001205" unit="g/cc"/>
   <fraction n="0.781154" ref="nitrogen"/>
   <fraction n="0.209476" ref="oxygen"/>
   <fraction n="0.00934" ref="argon"/>
  </material>

  <material formula=" " name="G10">
   <D value="1.7" unit="g/cc"/>
   <fraction n="0.2805" ref="silicon"/>
   <fraction n="0.3954" ref="oxygen"/>
   <fraction n="0.2990" ref="carbon"/>
   <fraction n="0.0251" ref="hydrogen"/>
  </material>

  <material formula=" " name="Granite">
   <D value="2.7" unit="g/cc"/>
   <fraction n="0.438" ref="oxygen"/>
   <fraction n="0.257" ref="silicon"/>
   <fraction n="0.222" ref="sodium"/>
   <fraction n="0.049" ref="aluminum"/>
   <fraction n="0.019" ref="iron"/>
   <fraction n="0.015" ref="potassium"/>
  </material>

  <material formula=" " name="ShotRock">
   <D value="2.7*0.6" unit="g/cc"/>
   <fraction n="0.438" ref="oxygen"/>
   <fraction n="0.257" ref="silicon"/>
   <fraction n="0.222" ref="sodium"/>
   <fraction n="0.049" ref="aluminum"/>
   <fraction n="0.019" ref="iron"/>
   <fraction n="0.015" ref="potassium"/>
  </material>

  <material formula=" " name="Dirt">
   <D value="1.7" unit="g/cc"/>
   <fraction n="0.438" ref="oxygen"/>
   <fraction n="0.257" ref="silicon"/>
   <fraction n="0.222" ref="sodium"/>
   <fraction n="0.049" ref="aluminum"/>
   <fraction n="0.019" ref="iron"/>
   <fraction n="0.015" ref="potassium"/>
  </material>

  <material formula=" " name="Concrete">
   <D value="2.3" unit="g/cc"/>
   <fraction n="0.530" ref="oxygen"/>
   <fraction n="0.335" ref="silicon"/>
   <fraction n="0.060" ref="calcium"/>
   <fraction n="0.015" ref="sodium"/>
   <fraction n="0.020" ref="iron"/>
   <fraction n="0.040" ref="aluminum"/>
  </material>

  <material formula="H2O" name="Water">
   <D value="1.0" unit="g/cc"/>
   <fraction n="0.1119" ref="hydrogen"/>
   <fraction n="0.8881" ref="oxygen"/>
  </material>

  <material formula="Ti" name="Titanium">
   <D value="4.506" unit="g/cc"/>
   <fraction n="1." ref="titanium"/>
  </material>

  <material name="TPB" formula="TPB">
   <D value="1.40" unit="g/cm3"/>
   <fraction n="1.0000" ref="argon"/>
  </material>

  <material name="Glass">
   <D value="2.74351" unit="g/cm3"/>
   <fraction n="0.600" ref="SiO2"/>
   <fraction n="0.118" ref="Al2O3"/>
   <fraction n="0.001" ref="Fe2O3"/>
   <fraction n="0.224" ref="CaO"/>
   <fraction n="0.034" ref="MgO"/>
   <fraction n="0.010" ref="Na2O"/>
   <fraction n="0.013" ref="TiO2"/>
  </material>

  <material name="Acrylic">
   <D value="1.19" unit="g/cm3"/>
   <fraction n="0.600" ref="carbon"/>
   <fraction n="0.320" ref="oxygen"/>
   <fraction n="0.080" ref="hydrogen"/>
  </material>

</materials>
EOF
}
