const {load,near,summary}=require('./harness');
const c=load('petroleum economics calculator.html');
if(c.__loadError)console.log('load:',c.__loadError);
// Project: CAPEX 100 M (60 % year 0, 40 % year 1), 1,000 bopd flat (plateau 20 yr), 70 USD/bbl, no royalty, OPEX 5 M/yr, tax 30 %
const p={capex:100,opex_annual:5,plateau_bopd:1000,plateau_yrs:20,royalty:0,tax:30};
const cf=c.genCashflows(p,70,6);
// Year 1: revenue 0.5 x 1000 x 365 x 70 = 12.775 M; taxable = 12.775 - 5 - 20 = -12.225 (loss carried)
near('year 0 CF',cf[0],-60,1e-9);
near('year 1 CF (no tax, loss)',cf[1],12.775-5-40,1e-9);
// Year 2: revenue 25.55; taxable = 25.55 - 5 - 20 - 12.225 = -11.675 -> no tax
near('year 2 CF (loss absorbs tax)',cf[2],25.55-5,1e-9);
// Year 3: taxable = 25.55 - 5 - 20 - 11.675 = -11.125 -> no tax; year 4 same pattern; year 6: no depreciation
// Year 6: cumulative losses: y3 -11.125, y4 -10.575, y5 -10.025; y6 taxable = 20.55 - 10.025 = 10.525 -> tax 3.1575
near('year 6 CF',cf[6],25.55-5-0.3*(25.55-5-10.025),1e-9);
summary();
