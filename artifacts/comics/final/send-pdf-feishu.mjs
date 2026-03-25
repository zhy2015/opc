import * as Lark from '@larksuiteoapi/node-sdk';
import fs from 'node:fs';
import os from 'node:os';

const APP_ID = process.env.FEISHU_APP_ID || 'cli_a9f68bc06f3a5bc7';
const APP_SECRET_PATH = (process.env.FEISHU_APP_SECRET_PATH || '~/.openclaw/secrets/feishu_app_secret').replace(/^~/, os.homedir());
const RECEIVE_ID = process.argv[2];
const FILE_PATH = process.argv[3];

if (!RECEIVE_ID || !FILE_PATH) throw new Error('usage: node send-pdf-feishu.mjs <open_id> <pdf_path>');
const APP_SECRET = fs.readFileSync(APP_SECRET_PATH, 'utf8').trim();
const client = new Lark.Client({
  appId: APP_ID,
  appSecret: APP_SECRET,
  domain: Lark.Domain.Feishu,
  appType: Lark.AppType.SelfBuild,
});

const fileStream = fs.createReadStream(FILE_PATH);
const fileName = FILE_PATH.split('/').pop();

const uploadRes = await client.im.v1.file.create({
  data: {
    file_type: 'pdf',
    file_name: fileName,
    file: fileStream,
  },
});
console.log('UPLOAD', JSON.stringify(uploadRes, null, 2));
const fileKey = uploadRes.data?.file_key || uploadRes.file_key;
if (!fileKey) throw new Error('no file_key returned');

const sendRes = await client.im.v1.message.create({
  params: { receive_id_type: 'open_id' },
  data: {
    receive_id: RECEIVE_ID,
    msg_type: 'file',
    content: JSON.stringify({ file_key: fileKey }),
  },
});
console.log('SEND', JSON.stringify(sendRes, null, 2));
