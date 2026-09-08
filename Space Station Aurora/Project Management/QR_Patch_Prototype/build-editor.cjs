const fs=require('fs'),path=require('path');
let html=fs.readFileSync(path.join(__dirname,'editor-template.html'),'utf8');
for(const [marker,file] of [['QRCODE_BUNDLE','qrcode-1.5.1.js'],['JSQR_BUNDLE','jsqr-1.4.0.js'],['JSZIP_BUNDLE','jszip-3.10.1.js']]){
 const js=fs.readFileSync(path.join(__dirname,file),'utf8').replace(/<\/script/gi,'<\\/script');
 html=html.replace('/* '+marker+' */',()=>js);
}
fs.writeFileSync(path.join(__dirname,'Aurora_QR_Patch_Editor.html'),html);
console.log('Created standalone QR patch editor.');
