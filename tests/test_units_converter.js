const {load,near,summary}=require('./harness');
const c=load('oilfield_units_converter.html');
if(c.__loadError)console.log('load:',c.__loadError);
function cv(id,v,fu,tu){c.__els['v-'+id].value=String(v);c.__els['fu-'+id].value=fu;c.__els['tu-'+id].value=tu;c.conv(id);
  return parseFloat(c.__els['rv-'+id].textContent.replace(/,/g,''));}
// Exact definitions: NIST SP 811 / SI Brochure
near('1 ft -> m',cv('len',1,'ft','m'),0.3048,1e-6);
near('1 lb -> kg',cv('mass',1,'lb','kg'),0.453592,1e-4);
near('1 m3 -> bbl',cv('vol',1,'m3','bbl'),6.28981,1e-5);
near('1000 psi -> bar',cv('press',1000,'psi','bar'),68.9476,1e-5);
near('10 ppg -> kg/m3',cv('dens',10,'ppg','kg/m3'),1198.26,1e-4);
near('1 psi/ft -> ppg (19.25)',cv('dens',1,'psi/ft','ppg'),19.25,2e-3);
near('1 bar/m -> SG',cv('dens',1,'bar/m','SG'),10.197,1e-3);
near('1 D -> m2',cv('perm',1,'D (Darcy)','m2'),9.869233e-13,1e-4);
near('100 degF -> degC',cv('temp',100,'°F','°C'),37.7778,1e-5);
near('1 HP(US) -> kW',cv('power',1,'HP(US)','kW'),0.7457,1e-4);
summary();
