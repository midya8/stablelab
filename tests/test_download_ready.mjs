import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import support from './chrome_support.cjs';
const delay=ms=>new Promise(r=>setTimeout(r,ms));
test('download readiness waits for bytes and temporary-file completion, without parsing retries',async()=>{
 const dir=fs.mkdtempSync(path.join(os.tmpdir(),'stablelab-download-')),file=path.join(dir,'evidence.json'),text=JSON.stringify({complete:true});
 try {
  fs.writeFileSync(file,'');fs.writeFileSync(file+'.crdownload','');
  let done=false;const pending=support.waitForDownload(file,Buffer.byteLength(text),{timeoutMs:2000,pollMs:5}).then(()=>done=true);
  await delay(25);assert.equal(done,false,'empty destination is not completion');
  fs.writeFileSync(file,text.slice(0,4));await delay(25);assert.equal(done,false,'partial bytes are not completion');
  fs.writeFileSync(file,text);await delay(25);assert.equal(done,false,'temporary file still indicates transfer');
  fs.unlinkSync(file+'.crdownload');await pending;assert.equal(done,true);assert.deepEqual(JSON.parse(fs.readFileSync(file)),{complete:true});
  fs.writeFileSync(file,'');await assert.rejects(support.waitForDownload(file,text.length,{timeoutMs:30,pollMs:5}),/did not complete/);
  fs.writeFileSync(file,text+'x');await assert.rejects(support.waitForDownload(file,text.length),/exceeds expected/);
  fs.writeFileSync(file,'x'.repeat(text.length));await support.waitForDownload(file,text.length);assert.throws(()=>JSON.parse(fs.readFileSync(file)),SyntaxError,'semantic corruption must not be retried');
 } finally {fs.rmSync(dir,{recursive:true,force:true});}
});
