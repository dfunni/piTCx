<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE eagle SYSTEM "eagle.dtd">
<eagle version="9.6.2">
<drawing>
<settings>
<setting alwaysvectorfont="no"/>
<setting verticaltext="up"/>
</settings>
<grid distance="0.1" unitdist="inch" unit="inch" style="lines" multiple="1" display="no" altdistance="0.01" altunitdist="inch" altunit="inch"/>
<layers>
<layer number="1" name="Top" color="4" fill="1" visible="no" active="no"/>
<layer number="16" name="Bottom" color="1" fill="1" visible="no" active="no"/>
<layer number="17" name="Pads" color="2" fill="1" visible="no" active="no"/>
<layer number="18" name="Vias" color="2" fill="1" visible="no" active="no"/>
<layer number="19" name="Unrouted" color="6" fill="1" visible="no" active="no"/>
<layer number="20" name="Dimension" color="24" fill="1" visible="no" active="no"/>
<layer number="21" name="tPlace" color="7" fill="1" visible="no" active="no"/>
<layer number="22" name="bPlace" color="7" fill="1" visible="no" active="no"/>
<layer number="23" name="tOrigins" color="15" fill="1" visible="no" active="no"/>
<layer number="24" name="bOrigins" color="15" fill="1" visible="no" active="no"/>
<layer number="25" name="tNames" color="7" fill="1" visible="no" active="no"/>
<layer number="26" name="bNames" color="7" fill="1" visible="no" active="no"/>
<layer number="27" name="tValues" color="7" fill="1" visible="no" active="no"/>
<layer number="28" name="bValues" color="7" fill="1" visible="no" active="no"/>
<layer number="29" name="tStop" color="7" fill="3" visible="no" active="no"/>
<layer number="30" name="bStop" color="7" fill="6" visible="no" active="no"/>
<layer number="31" name="tCream" color="7" fill="4" visible="no" active="no"/>
<layer number="32" name="bCream" color="7" fill="5" visible="no" active="no"/>
<layer number="33" name="tFinish" color="6" fill="3" visible="no" active="no"/>
<layer number="34" name="bFinish" color="6" fill="6" visible="no" active="no"/>
<layer number="35" name="tGlue" color="7" fill="4" visible="no" active="no"/>
<layer number="36" name="bGlue" color="7" fill="5" visible="no" active="no"/>
<layer number="37" name="tTest" color="7" fill="1" visible="no" active="no"/>
<layer number="38" name="bTest" color="7" fill="1" visible="no" active="no"/>
<layer number="39" name="tKeepout" color="4" fill="11" visible="no" active="no"/>
<layer number="40" name="bKeepout" color="1" fill="11" visible="no" active="no"/>
<layer number="41" name="tRestrict" color="4" fill="10" visible="no" active="no"/>
<layer number="42" name="bRestrict" color="1" fill="10" visible="no" active="no"/>
<layer number="43" name="vRestrict" color="2" fill="10" visible="no" active="no"/>
<layer number="44" name="Drills" color="7" fill="1" visible="no" active="no"/>
<layer number="45" name="Holes" color="7" fill="1" visible="no" active="no"/>
<layer number="46" name="Milling" color="3" fill="1" visible="no" active="no"/>
<layer number="47" name="Measures" color="7" fill="1" visible="no" active="no"/>
<layer number="48" name="Document" color="7" fill="1" visible="no" active="no"/>
<layer number="49" name="Reference" color="7" fill="1" visible="no" active="no"/>
<layer number="51" name="tDocu" color="7" fill="1" visible="no" active="no"/>
<layer number="52" name="bDocu" color="7" fill="1" visible="no" active="no"/>
<layer number="88" name="SimResults" color="9" fill="1" visible="yes" active="yes"/>
<layer number="89" name="SimProbes" color="9" fill="1" visible="yes" active="yes"/>
<layer number="90" name="Modules" color="5" fill="1" visible="yes" active="yes"/>
<layer number="91" name="Nets" color="2" fill="1" visible="yes" active="yes"/>
<layer number="92" name="Busses" color="1" fill="1" visible="yes" active="yes"/>
<layer number="93" name="Pins" color="2" fill="1" visible="no" active="yes"/>
<layer number="94" name="Symbols" color="4" fill="1" visible="yes" active="yes"/>
<layer number="95" name="Names" color="7" fill="1" visible="yes" active="yes"/>
<layer number="96" name="Values" color="7" fill="1" visible="yes" active="yes"/>
<layer number="97" name="Info" color="7" fill="1" visible="yes" active="yes"/>
<layer number="98" name="Guide" color="6" fill="1" visible="yes" active="yes"/>
</layers>
<schematic xreflabel="%F%N/%S.%C%R" xrefpart="/%S.%C%R">
<libraries>
<library name="Power Supplies">
<packages>
<package name="PAA30B-10">
<wire x1="0" y1="0" x2="64.3" y2="0" width="0.3048" layer="21"/>
<wire x1="64.3" y1="0" x2="64.3" y2="45.1" width="0.3048" layer="21"/>
<wire x1="64.3" y1="45.1" x2="0" y2="45.1" width="0.3048" layer="21"/>
<wire x1="0" y1="45.1" x2="0" y2="0" width="0.3048" layer="21"/>
<pad name="AC_IN(L)" x="4.15" y="5.05" drill="1.2" diameter="2.54"/>
<pad name="AC_IN(N)" x="4.15" y="22.55" drill="1.2" diameter="2.54"/>
<pad name="NO_PIN" x="58.15" y="22.5" drill="1.2" diameter="2.54"/>
<pad name="+DC_OUT" x="58.15" y="12.55" drill="1.2" diameter="2.54"/>
<pad name="-DC_OUT" x="58.15" y="33.55" drill="1.2" diameter="2.54"/>
<text x="1.27" y="40.64" size="1.27" layer="21">&gt;Value</text>
<text x="1.27" y="43.18" size="1.27" layer="21">&gt;Name</text>
</package>
</packages>
<symbols>
<symbol name="PAA30B-10">
<wire x1="0" y1="0" x2="27.94" y2="0" width="0.254" layer="94"/>
<wire x1="27.94" y1="0" x2="27.94" y2="15.24" width="0.254" layer="94"/>
<wire x1="0" y1="15.24" x2="0" y2="0" width="0.254" layer="94"/>
<pin name="AC_IN(N)" x="-5.08" y="12.7" visible="pin" length="middle" direction="in"/>
<pin name="AC_IN(L)" x="-5.08" y="2.54" visible="pin" length="middle" direction="in"/>
<pin name="-DC_OUT" x="33.02" y="12.7" visible="pin" length="middle" direction="out" rot="R180"/>
<pin name="NO_PIN" x="33.02" y="7.62" visible="pin" length="middle" direction="nc" rot="R180"/>
<pin name="+DC_OUT" x="33.02" y="2.54" visible="pin" length="middle" direction="out" rot="R180"/>
<wire x1="0" y1="15.24" x2="27.94" y2="15.24" width="0.254" layer="94"/>
<text x="0" y="17.78" size="1.27" layer="97">&gt;Name</text>
<text x="22.86" y="17.78" size="1.27" layer="97">&gt;Value</text>
</symbol>
</symbols>
<devicesets>
<deviceset name="PAA30B-10">
<gates>
<gate name="G$1" symbol="PAA30B-10" x="-10.16" y="5.08"/>
</gates>
<devices>
<device name="" package="PAA30B-10">
<connects>
<connect gate="G$1" pin="+DC_OUT" pad="+DC_OUT"/>
<connect gate="G$1" pin="-DC_OUT" pad="-DC_OUT"/>
<connect gate="G$1" pin="AC_IN(L)" pad="AC_IN(L)"/>
<connect gate="G$1" pin="AC_IN(N)" pad="AC_IN(N)"/>
<connect gate="G$1" pin="NO_PIN" pad="NO_PIN"/>
</connects>
<technologies>
<technology name=""/>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
<library name="PCB_TERM_BLK_WAGO_2604-1104">
<packages>
<package name="TERM_BLK_WAGO_2604-1104">
<pad name="P0" x="15" y="0" drill="1.3" diameter="2.5" rot="R270"/>
<pad name="P1" x="10" y="0" drill="1.3" diameter="2.5" rot="R270"/>
<pad name="P2" x="5" y="0" drill="1.3" diameter="2.5" rot="R270"/>
<pad name="P3" x="0" y="0" drill="1.3" diameter="2.5" rot="R90"/>
<pad name="P4" x="0" y="-8.2" drill="1.3" diameter="2.5" rot="R270"/>
<pad name="P5" x="5" y="-8.2" drill="1.3" diameter="2.5" rot="R270"/>
<pad name="P6" x="10" y="-8.2" drill="1.3" diameter="2.5" rot="R270"/>
<pad name="P7" x="15" y="-8.2" drill="1.3" diameter="2.5" rot="R270"/>
<text x="-3.685334375" y="3.865" size="1.27" layer="25">&gt;NAME</text>
<wire x1="18.8" y1="-13.4" x2="17.5" y2="-13.4" width="0.127" layer="48"/>
<wire x1="17.5" y1="-13.4" x2="12.5" y2="-13.4" width="0.127" layer="48"/>
<wire x1="12.5" y1="-13.4" x2="7.5" y2="-13.4" width="0.127" layer="48"/>
<wire x1="7.5" y1="-13.4" x2="2.5" y2="-13.4" width="0.127" layer="48"/>
<wire x1="2.5" y1="-13.4" x2="-2.7" y2="-13.4" width="0.127" layer="48"/>
<wire x1="-2.7" y1="-13.4" x2="-3.6" y2="-13.4" width="0.127" layer="48"/>
<wire x1="-3.6" y1="-13.4" x2="-3.6" y2="2.9" width="0.127" layer="48"/>
<wire x1="-3.6" y1="2.9" x2="-2.7" y2="2.9" width="0.127" layer="48"/>
<wire x1="-2.7" y1="2.9" x2="2.5" y2="2.9" width="0.127" layer="48"/>
<wire x1="2.5" y1="2.9" x2="7.5" y2="2.9" width="0.127" layer="48"/>
<wire x1="7.5" y1="2.9" x2="12.5" y2="2.9" width="0.127" layer="48"/>
<wire x1="12.5" y1="2.9" x2="17.5" y2="2.9" width="0.127" layer="48"/>
<wire x1="17.5" y1="2.9" x2="18.8" y2="2.9" width="0.127" layer="48"/>
<wire x1="18.8" y1="2.9" x2="18.8" y2="-13.4" width="0.127" layer="48"/>
<wire x1="2.5" y1="2.9" x2="2.5" y2="-13.4" width="0.127" layer="48"/>
<wire x1="7.5" y1="2.9" x2="7.5" y2="-13.4" width="0.127" layer="48"/>
<wire x1="12.5" y1="2.9" x2="12.5" y2="-13.4" width="0.127" layer="48"/>
<wire x1="17.5" y1="2.9" x2="17.5" y2="-13.4" width="0.127" layer="48"/>
<wire x1="-2.7" y1="2.9" x2="-2.7" y2="-13.4" width="0.127" layer="48"/>
<text x="13.97" y="3.81" size="1.27" layer="21">&gt;Value</text>
</package>
</packages>
<symbols>
<symbol name="TERM_BLK_WAGO_2604-1104">
<pin name="P$1" x="5.08" y="-5.08" visible="pin" length="middle" rot="R90"/>
<pin name="P$2" x="10.16" y="-5.08" visible="pin" length="middle" rot="R90"/>
<pin name="P$3" x="15.24" y="-5.08" visible="pin" length="middle" rot="R90"/>
<pin name="P$4" x="20.32" y="-5.08" visible="pin" length="middle" rot="R90"/>
<wire x1="0" y1="0" x2="25.4" y2="0" width="0.254" layer="94"/>
<wire x1="25.4" y1="0" x2="25.4" y2="15.24" width="0.254" layer="94"/>
<wire x1="25.4" y1="15.24" x2="0" y2="15.24" width="0.254" layer="94"/>
<wire x1="0" y1="15.24" x2="0" y2="0" width="0.254" layer="94"/>
<text x="0" y="15.748" size="1.27" layer="97">&gt;Name</text>
<text x="20.32" y="15.748" size="1.27" layer="97">&gt;Value</text>
</symbol>
</symbols>
<devicesets>
<deviceset name="TERM_BLK_WAGO_2604-1104">
<gates>
<gate name="G$1" symbol="TERM_BLK_WAGO_2604-1104" x="0" y="0"/>
</gates>
<devices>
<device name="" package="TERM_BLK_WAGO_2604-1104">
<connects>
<connect gate="G$1" pin="P$1" pad="P3 P4"/>
<connect gate="G$1" pin="P$2" pad="P2 P5"/>
<connect gate="G$1" pin="P$3" pad="P1 P6"/>
<connect gate="G$1" pin="P$4" pad="P0 P7"/>
</connects>
<technologies>
<technology name=""/>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
<library name="Crydom">
<packages>
<package name="RELAY_PF">
<pad name="1" x="0" y="0" drill="1.3" diameter="2.1844" shape="long"/>
<pad name="2" x="0" y="-10.16" drill="1.3" diameter="2.1844" shape="long"/>
<pad name="7" x="0" y="-22.86" drill="1.3" diameter="2.1844" shape="long"/>
<pad name="9" x="0" y="-27.94" drill="1.3" diameter="2.1844" shape="long"/>
<wire x1="-4.572" y1="-13.97" x2="-4.572" y2="13.081" width="0.1524" layer="47"/>
<wire x1="18.288" y1="-13.97" x2="18.288" y2="13.081" width="0.1524" layer="47"/>
<wire x1="-4.572" y1="12.7" x2="18.288" y2="12.7" width="0.1524" layer="47"/>
<wire x1="-4.572" y1="12.7" x2="-4.318" y2="12.827" width="0.1524" layer="47"/>
<wire x1="-4.572" y1="12.7" x2="-4.318" y2="12.573" width="0.1524" layer="47"/>
<wire x1="-4.318" y1="12.827" x2="-4.318" y2="12.573" width="0.1524" layer="47"/>
<wire x1="18.288" y1="12.7" x2="18.034" y2="12.827" width="0.1524" layer="47"/>
<wire x1="18.288" y1="12.7" x2="18.034" y2="12.573" width="0.1524" layer="47"/>
<wire x1="18.034" y1="12.827" x2="18.034" y2="12.573" width="0.1524" layer="47"/>
<wire x1="0" y1="-13.97" x2="0" y2="10.541" width="0.1524" layer="47"/>
<wire x1="13.716" y1="-13.97" x2="13.716" y2="10.541" width="0.1524" layer="47"/>
<wire x1="0" y1="10.16" x2="13.716" y2="10.16" width="0.1524" layer="47"/>
<wire x1="0" y1="10.16" x2="0.254" y2="10.287" width="0.1524" layer="47"/>
<wire x1="0" y1="10.16" x2="0.254" y2="10.033" width="0.1524" layer="47"/>
<wire x1="0.254" y1="10.287" x2="0.254" y2="10.033" width="0.1524" layer="47"/>
<wire x1="13.716" y1="10.16" x2="13.462" y2="10.287" width="0.1524" layer="47"/>
<wire x1="13.716" y1="10.16" x2="13.462" y2="10.033" width="0.1524" layer="47"/>
<wire x1="13.462" y1="10.287" x2="13.462" y2="10.033" width="0.1524" layer="47"/>
<wire x1="18.288" y1="0" x2="-10.033" y2="0" width="0.1524" layer="47"/>
<wire x1="-9.652" y1="7.62" x2="-9.652" y2="0" width="0.1524" layer="47"/>
<wire x1="-9.652" y1="7.62" x2="-9.779" y2="7.366" width="0.1524" layer="47"/>
<wire x1="-9.652" y1="7.62" x2="-9.525" y2="7.366" width="0.1524" layer="47"/>
<wire x1="-9.779" y1="7.366" x2="-9.525" y2="7.366" width="0.1524" layer="47"/>
<wire x1="-9.652" y1="0" x2="-9.779" y2="0.254" width="0.1524" layer="47"/>
<wire x1="-9.652" y1="0" x2="-9.525" y2="0.254" width="0.1524" layer="47"/>
<wire x1="-9.779" y1="0.254" x2="-9.525" y2="0.254" width="0.1524" layer="47"/>
<wire x1="6.858" y1="0" x2="26.289" y2="0" width="0.1524" layer="47"/>
<wire x1="18.288" y1="-10.16" x2="26.289" y2="-10.16" width="0.1524" layer="47"/>
<wire x1="25.908" y1="0" x2="25.908" y2="-10.16" width="0.1524" layer="47"/>
<wire x1="25.908" y1="0" x2="25.781" y2="-0.254" width="0.1524" layer="47"/>
<wire x1="25.908" y1="0" x2="26.035" y2="-0.254" width="0.1524" layer="47"/>
<wire x1="25.781" y1="-0.254" x2="26.035" y2="-0.254" width="0.1524" layer="47"/>
<wire x1="25.908" y1="-10.16" x2="25.781" y2="-9.906" width="0.1524" layer="47"/>
<wire x1="25.908" y1="-10.16" x2="26.035" y2="-9.906" width="0.1524" layer="47"/>
<wire x1="25.781" y1="-9.906" x2="26.035" y2="-9.906" width="0.1524" layer="47"/>
<wire x1="-10.033" y1="7.62" x2="28.829" y2="7.62" width="0.1524" layer="47"/>
<wire x1="18.288" y1="-35.56" x2="28.829" y2="-35.56" width="0.1524" layer="47"/>
<wire x1="28.448" y1="7.62" x2="28.448" y2="-35.56" width="0.1524" layer="47"/>
<wire x1="28.448" y1="7.62" x2="28.321" y2="7.366" width="0.1524" layer="47"/>
<wire x1="28.448" y1="7.62" x2="28.575" y2="7.366" width="0.1524" layer="47"/>
<wire x1="28.321" y1="7.366" x2="28.575" y2="7.366" width="0.1524" layer="47"/>
<wire x1="28.448" y1="-35.56" x2="28.321" y2="-35.306" width="0.1524" layer="47"/>
<wire x1="28.448" y1="-35.56" x2="28.575" y2="-35.306" width="0.1524" layer="47"/>
<wire x1="28.321" y1="-35.306" x2="28.575" y2="-35.306" width="0.1524" layer="47"/>
<text x="-8.9217" y="-40.64" size="1.27" layer="47" ratio="6">Default Padstyle: EX70Y70D50P</text>
<text x="-7.9556" y="-42.164" size="1.27" layer="47" ratio="6">Alt 1 Padstyle: OX60Y90D30P</text>
<text x="-7.9556" y="-43.688" size="1.27" layer="47" ratio="6">Alt 2 Padstyle: OX90Y60D30P</text>
<text x="3.3919" y="13.208" size="0.635" layer="47" ratio="4">0.9in/22.86mm</text>
<text x="2.8156" y="10.668" size="0.635" layer="47" ratio="4">0.54in/13.716mm</text>
<text x="-16.516" y="3.4925" size="0.635" layer="47" ratio="4">0.3in/7.62mm</text>
<text x="26.416" y="-5.3975" size="0.635" layer="47" ratio="4">0.4in/10.16mm</text>
<text x="28.956" y="-14.2875" size="0.635" layer="47" ratio="4">1.7in/43.18mm</text>
<wire x1="-4.699" y1="-35.687" x2="18.415" y2="-35.687" width="0.1524" layer="21"/>
<wire x1="18.415" y1="-35.687" x2="18.415" y2="7.747" width="0.1524" layer="21"/>
<wire x1="18.415" y1="7.747" x2="-4.699" y2="7.747" width="0.1524" layer="21"/>
<wire x1="-4.699" y1="7.747" x2="-4.699" y2="-35.687" width="0.1524" layer="21"/>
<wire x1="-4.572" y1="-35.56" x2="18.288" y2="-35.56" width="0.1524" layer="51"/>
<wire x1="18.288" y1="-35.56" x2="18.288" y2="7.62" width="0.1524" layer="51"/>
<wire x1="18.288" y1="7.62" x2="-4.572" y2="7.62" width="0.1524" layer="51"/>
<wire x1="-4.572" y1="7.62" x2="-4.572" y2="-35.56" width="0.1524" layer="51"/>
<wire x1="7.1628" y1="7.62" x2="6.5532" y2="7.62" width="0.1524" layer="51" curve="-180"/>
<text x="-2.7632" y="5.715" size="1.27" layer="27" ratio="6">&gt;Name</text>
<text x="-2.4908" y="-33.655" size="1.27" layer="27" ratio="6">&gt;Value</text>
</package>
</packages>
<symbols>
<symbol name="PF240D25">
<pin name="AC_LOAD_2" x="2.54" y="2.54" length="middle" direction="pas"/>
<pin name="AC_LOAD" x="2.54" y="-5.08" length="middle" direction="pas"/>
<pin name="DC_CONTROL+" x="53.34" y="-5.08" length="middle" direction="pas" rot="R180"/>
<pin name="DC_CONTROL-" x="53.34" y="2.54" length="middle" direction="pas" rot="R180"/>
<wire x1="7.62" y1="5.08" x2="7.62" y2="-7.62" width="0.1524" layer="94"/>
<wire x1="7.62" y1="-7.62" x2="48.26" y2="-7.62" width="0.1524" layer="94"/>
<wire x1="48.26" y1="-7.62" x2="48.26" y2="5.08" width="0.1524" layer="94"/>
<wire x1="48.26" y1="5.08" x2="7.62" y2="5.08" width="0.1524" layer="94"/>
<text x="35.9146" y="9.1186" size="2.083" layer="95" ratio="6">&gt;Name</text>
<text x="35.2752" y="6.5786" size="2.083" layer="96" ratio="6">&gt;Value</text>
</symbol>
</symbols>
<devicesets>
<deviceset name="PF240D25" prefix="U">
<gates>
<gate name="A" symbol="PF240D25" x="0" y="0"/>
</gates>
<devices>
<device name="RELAY_PF" package="RELAY_PF">
<connects>
<connect gate="A" pin="AC_LOAD" pad="2"/>
<connect gate="A" pin="AC_LOAD_2" pad="1"/>
<connect gate="A" pin="DC_CONTROL+" pad="7"/>
<connect gate="A" pin="DC_CONTROL-" pad="9"/>
</connects>
<technologies>
<technology name="">
<attribute name="COPYRIGHT" value="Copyright (C) 2023 Ultra Librarian. All rights reserved." constant="no"/>
<attribute name="MANUFACTURER_PART_NUMBER" value="PF240D25" constant="no"/>
<attribute name="MFR_NAME" value="Sensata / Crydom" constant="no"/>
</technology>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
<library name="436500414">
<packages>
<package name="CON_436500414">
<smd name="1" x="4.5" y="5.12" dx="1.27" dy="2.92" layer="1"/>
<smd name="2" x="1.5" y="5.12" dx="1.27" dy="2.92" layer="1"/>
<smd name="3" x="-1.5" y="5.12" dx="1.27" dy="2.92" layer="1"/>
<smd name="4" x="-4.5" y="5.12" dx="1.27" dy="2.92" layer="1"/>
<smd name="P1" x="8.385" y="-0.35" dx="3.43" dy="1.65" layer="1"/>
<smd name="P2" x="-8.385" y="-0.35" dx="3.43" dy="1.65" layer="1"/>
<wire x1="10.079" y1="5.12" x2="11.349" y2="5.755" width="0.1524" layer="51"/>
<wire x1="11.349" y1="5.755" x2="11.349" y2="4.485" width="0.1524" layer="51"/>
<wire x1="11.349" y1="4.485" x2="10.079" y2="5.12" width="0.1524" layer="51"/>
<wire x1="-9.825" y1="-4.95" x2="9.825" y2="-4.95" width="0.1524" layer="51"/>
<wire x1="9.825" y1="-4.95" x2="9.825" y2="5.75" width="0.1524" layer="51"/>
<wire x1="9.825" y1="5.75" x2="-9.825" y2="5.75" width="0.1524" layer="51"/>
<wire x1="-9.825" y1="5.75" x2="-9.825" y2="-4.95" width="0.1524" layer="51"/>
<text x="-5.1864" y="13.1" size="1.27" layer="51" ratio="6">436500414</text>
<wire x1="10.079" y1="5.12" x2="11.349" y2="5.755" width="0.1524" layer="21"/>
<wire x1="11.349" y1="5.755" x2="11.349" y2="4.485" width="0.1524" layer="21"/>
<wire x1="11.349" y1="4.485" x2="10.079" y2="5.12" width="0.1524" layer="21"/>
<wire x1="-9.825" y1="5.75" x2="-9.825" y2="0.795" width="0.1524" layer="21"/>
<wire x1="-9.825" y1="-4.95" x2="9.825" y2="-4.95" width="0.1524" layer="21"/>
<wire x1="9.825" y1="-4.95" x2="9.825" y2="-1.4951" width="0.1524" layer="21"/>
<wire x1="9.825" y1="5.75" x2="5.455" y2="5.75" width="0.1524" layer="21"/>
<wire x1="3.545" y1="5.75" x2="2.455" y2="5.75" width="0.1524" layer="21"/>
<wire x1="0.545" y1="5.75" x2="-0.545" y2="5.75" width="0.1524" layer="21"/>
<wire x1="-2.455" y1="5.75" x2="-3.545" y2="5.75" width="0.1524" layer="21"/>
<wire x1="-5.455" y1="5.75" x2="-9.825" y2="5.75" width="0.1524" layer="21"/>
<wire x1="9.825" y1="0.795" x2="9.825" y2="5.75" width="0.1524" layer="21"/>
<wire x1="-9.825" y1="-1.4951" x2="-9.825" y2="-4.95" width="0.1524" layer="21"/>
<text x="-5.1864" y="13.1" size="1.27" layer="21" ratio="6">436500414</text>
<text x="-3.2712" y="9.525" size="1.27" layer="27" ratio="6">&gt;Name</text>
<text x="-1.7288" y="9.525" size="1.27" layer="27" ratio="6">&gt;Value</text>
</package>
</packages>
<symbols>
<symbol name="CON_436500414">
<pin name="1" x="0" y="0" visible="pad" length="middle" direction="pas"/>
<pin name="2" x="0" y="-2.54" visible="pad" length="middle" direction="pas"/>
<pin name="3" x="0" y="-5.08" visible="pad" length="middle" direction="pas"/>
<pin name="4" x="0" y="-7.62" visible="pad" length="middle" direction="pas"/>
<pin name="P1" x="0" y="-10.16" visible="pad" length="middle" direction="pas"/>
<pin name="P2" x="0" y="-12.7" visible="pad" length="middle" direction="pas"/>
<wire x1="10.16" y1="0" x2="5.08" y2="0" width="0.1524" layer="94"/>
<wire x1="10.16" y1="-2.54" x2="5.08" y2="-2.54" width="0.1524" layer="94"/>
<wire x1="10.16" y1="-5.08" x2="5.08" y2="-5.08" width="0.1524" layer="94"/>
<wire x1="10.16" y1="-7.62" x2="5.08" y2="-7.62" width="0.1524" layer="94"/>
<wire x1="10.16" y1="-10.16" x2="5.08" y2="-10.16" width="0.1524" layer="94"/>
<wire x1="10.16" y1="-12.7" x2="5.08" y2="-12.7" width="0.1524" layer="94"/>
<wire x1="10.16" y1="0" x2="8.89" y2="0.8467" width="0.1524" layer="94"/>
<wire x1="10.16" y1="-2.54" x2="8.89" y2="-1.6933" width="0.1524" layer="94"/>
<wire x1="10.16" y1="-5.08" x2="8.89" y2="-4.2333" width="0.1524" layer="94"/>
<wire x1="10.16" y1="-7.62" x2="8.89" y2="-6.7733" width="0.1524" layer="94"/>
<wire x1="10.16" y1="-10.16" x2="8.89" y2="-9.3133" width="0.1524" layer="94"/>
<wire x1="10.16" y1="-12.7" x2="8.89" y2="-11.8533" width="0.1524" layer="94"/>
<wire x1="10.16" y1="0" x2="8.89" y2="-0.8467" width="0.1524" layer="94"/>
<wire x1="10.16" y1="-2.54" x2="8.89" y2="-3.3867" width="0.1524" layer="94"/>
<wire x1="10.16" y1="-5.08" x2="8.89" y2="-5.9267" width="0.1524" layer="94"/>
<wire x1="10.16" y1="-7.62" x2="8.89" y2="-8.4667" width="0.1524" layer="94"/>
<wire x1="10.16" y1="-10.16" x2="8.89" y2="-11.0067" width="0.1524" layer="94"/>
<wire x1="10.16" y1="-12.7" x2="8.89" y2="-13.5467" width="0.1524" layer="94"/>
<wire x1="5.08" y1="2.54" x2="5.08" y2="-15.24" width="0.1524" layer="94"/>
<wire x1="5.08" y1="-15.24" x2="12.7" y2="-15.24" width="0.1524" layer="94"/>
<wire x1="12.7" y1="-15.24" x2="12.7" y2="2.54" width="0.1524" layer="94"/>
<wire x1="12.7" y1="2.54" x2="5.08" y2="2.54" width="0.1524" layer="94"/>
<text x="4.1646" y="5.3086" size="2.083" layer="95" ratio="6">&gt;Name</text>
</symbol>
</symbols>
<devicesets>
<deviceset name="436500414" prefix="J">
<gates>
<gate name="A" symbol="CON_436500414" x="0" y="0"/>
</gates>
<devices>
<device name="CON_436500414" package="CON_436500414">
<connects>
<connect gate="A" pin="1" pad="1"/>
<connect gate="A" pin="2" pad="2"/>
<connect gate="A" pin="3" pad="3"/>
<connect gate="A" pin="4" pad="4"/>
<connect gate="A" pin="P1" pad="P1"/>
<connect gate="A" pin="P2" pad="P2"/>
</connects>
<technologies>
<technology name="">
<attribute name="COPYRIGHT" value="Copyright (C) 2024 Ultra Librarian. All rights reserved." constant="no"/>
<attribute name="MANUFACTURER_PART_NUMBER" value="436500414" constant="no"/>
<attribute name="MFR_NAME" value="Molex Connector Corporation" constant="no"/>
</technology>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
</libraries>
<attributes>
</attributes>
<variantdefs>
</variantdefs>
<classes>
<class number="0" name="default" width="0" drill="0">
</class>
</classes>
<parts>
<part name="U2" library="Power Supplies" deviceset="PAA30B-10" device=""/>
<part name="J2" library="PCB_TERM_BLK_WAGO_2604-1104" deviceset="TERM_BLK_WAGO_2604-1104" device=""/>
<part name="U1" library="Crydom" deviceset="PF240D25" device="RELAY_PF"/>
<part name="J3" library="436500414" deviceset="436500414" device="CON_436500414"/>
</parts>
<sheets>
<sheet>
<plain>
</plain>
<instances>
<instance part="U2" gate="G$1" x="86.36" y="35.56" smashed="yes">
<attribute name="NAME" x="114.046" y="52.832" size="1.27" layer="97" rot="R180"/>
<attribute name="VALUE" x="86.36" y="52.07" size="1.27" layer="97"/>
</instance>
<instance part="J2" gate="G$1" x="60.96" y="40.64" smashed="yes" rot="R90">
<attribute name="NAME" x="58.42" y="66.548" size="1.27" layer="97"/>
<attribute name="VALUE" x="63.5" y="40.132" size="1.27" layer="97" rot="R180"/>
</instance>
<instance part="U1" gate="A" x="78.74" y="68.58" smashed="yes">
<attribute name="NAME" x="114.6546" y="77.6986" size="2.083" layer="95" ratio="6"/>
<attribute name="VALUE" x="114.0152" y="75.1586" size="2.083" layer="96" ratio="6"/>
</instance>
<instance part="J3" gate="A" x="137.16" y="50.8" smashed="yes">
<attribute name="NAME" x="141.3246" y="56.1086" size="2.083" layer="95" ratio="6"/>
</instance>
</instances>
<busses>
</busses>
<nets>
<net name="AC_HEATER" class="0">
<segment>
<pinref part="U1" gate="A" pin="AC_LOAD_2"/>
<label x="66.04" y="71.12" size="1.778" layer="95"/>
<pinref part="J2" gate="G$1" pin="P$4"/>
<wire x1="66.04" y1="60.96" x2="73.66" y2="60.96" width="0.1524" layer="91"/>
<wire x1="73.66" y1="60.96" x2="73.66" y2="68.58" width="0.1524" layer="91"/>
<wire x1="81.28" y1="71.12" x2="73.66" y2="71.12" width="0.1524" layer="91"/>
<wire x1="73.66" y1="71.12" x2="73.66" y2="68.58" width="0.1524" layer="91"/>
</segment>
</net>
<net name="AC(L)" class="0">
<segment>
<pinref part="J2" gate="G$1" pin="P$3"/>
<wire x1="66.04" y1="55.88" x2="68.58" y2="55.88" width="0.1524" layer="91"/>
<pinref part="J2" gate="G$1" pin="P$2"/>
<wire x1="66.04" y1="50.8" x2="68.58" y2="50.8" width="0.1524" layer="91"/>
<pinref part="U2" gate="G$1" pin="AC_IN(L)"/>
<wire x1="68.58" y1="50.8" x2="68.58" y2="38.1" width="0.1524" layer="91"/>
<wire x1="68.58" y1="38.1" x2="81.28" y2="38.1" width="0.1524" layer="91"/>
<wire x1="68.58" y1="55.88" x2="68.58" y2="50.8" width="0.1524" layer="91"/>
<junction x="68.58" y="50.8"/>
<label x="71.12" y="38.1" size="1.778" layer="95"/>
</segment>
</net>
<net name="AC(N)" class="0">
<segment>
<pinref part="U2" gate="G$1" pin="AC_IN(N)"/>
<wire x1="81.28" y1="63.5" x2="81.28" y2="48.26" width="0.1524" layer="91"/>
<pinref part="U1" gate="A" pin="AC_LOAD"/>
<label x="76.2" y="58.42" size="1.778" layer="95"/>
<pinref part="J2" gate="G$1" pin="P$1"/>
<wire x1="66.04" y1="45.72" x2="81.28" y2="45.72" width="0.1524" layer="91"/>
<wire x1="81.28" y1="45.72" x2="81.28" y2="48.26" width="0.1524" layer="91"/>
<junction x="81.28" y="48.26"/>
</segment>
</net>
<net name="VCC" class="0">
<segment>
<pinref part="U2" gate="G$1" pin="+DC_OUT"/>
<wire x1="119.38" y1="38.1" x2="121.92" y2="38.1" width="0.1524" layer="91"/>
<label x="119.38" y="38.1" size="1.778" layer="95"/>
</segment>
<segment>
<wire x1="137.16" y1="48.26" x2="132.08" y2="48.26" width="0.1524" layer="91"/>
<label x="129.54" y="48.26" size="1.778" layer="95"/>
<pinref part="J3" gate="A" pin="2"/>
</segment>
</net>
<net name="OT1" class="0">
<segment>
<pinref part="U1" gate="A" pin="DC_CONTROL-"/>
<wire x1="134.62" y1="71.12" x2="132.08" y2="71.12" width="0.1524" layer="91"/>
<label x="132.08" y="71.12" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="J3" gate="A" pin="4"/>
<wire x1="137.16" y1="43.18" x2="132.08" y2="43.18" width="0.1524" layer="91"/>
<label x="129.54" y="43.18" size="1.778" layer="95"/>
</segment>
</net>
<net name="GND" class="0">
<segment>
<pinref part="U2" gate="G$1" pin="-DC_OUT"/>
<wire x1="119.38" y1="48.26" x2="121.92" y2="48.26" width="0.1524" layer="91"/>
<label x="119.38" y="48.26" size="1.778" layer="95"/>
</segment>
<segment>
<wire x1="137.16" y1="50.8" x2="132.08" y2="50.8" width="0.1524" layer="91"/>
<label x="129.54" y="50.8" size="1.778" layer="95"/>
<pinref part="J3" gate="A" pin="1"/>
</segment>
</net>
<net name="3.3V" class="0">
<segment>
<wire x1="137.16" y1="45.72" x2="132.08" y2="45.72" width="0.1524" layer="91"/>
<label x="129.54" y="45.72" size="1.778" layer="95"/>
<pinref part="J3" gate="A" pin="3"/>
</segment>
<segment>
<pinref part="U1" gate="A" pin="DC_CONTROL+"/>
<wire x1="132.08" y1="63.5" x2="134.62" y2="63.5" width="0.1524" layer="91"/>
<label x="132.08" y="63.5" size="1.778" layer="95"/>
</segment>
</net>
</nets>
</sheet>
</sheets>
</schematic>
</drawing>
</eagle>
