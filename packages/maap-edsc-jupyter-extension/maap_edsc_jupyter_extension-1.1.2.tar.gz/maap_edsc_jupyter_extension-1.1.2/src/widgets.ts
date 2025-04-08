import { Widget } from '@lumino/widgets';
import { PageConfig } from '@jupyterlab/coreutils'
import { Notification } from '@jupyterlab/apputils';

import {
  request, RequestResult
} from './request';

//import "./globals"
import globals from "./globals";

let unique = 0;

//
// Widget to display Earth Data Search Client inside an iframe
//
export
class IFrameWidget extends Widget {

  constructor(path: string) {
    super();
    this.id = path + '-' + unique;
    unique += 1;

    this.title.label = "Earthdata Search";
    this.title.closable = true;

    let div = document.createElement('div');
    div.classList.add('iframe-widget');
    let iframe = document.createElement('iframe');
    iframe.id = "iframeid";

    // set proxy to EDSC
    request('get', path).then((res: RequestResult) => {
      if (res.ok){
        iframe.src = path;
      } else {
        iframe.setAttribute('baseURI', PageConfig.getBaseUrl());
        if(res.status == 404){

        } else if(res.status == 401){

        } else {
          path = "edsc/proxy/" + path;
          iframe.src = path;
        }
      }
    });

    div.appendChild(iframe);
    this.node.appendChild(div);
  }
};

//
// Widget to display selected search parameter
//
export
class ParamsPopupWidget extends Widget {
  constructor() {
    let body = document.createElement('div');
    body.style.display = 'flex';
    body.style.flexDirection = 'column';
    
    let showGranuleParams = globals.granuleParams;
    let showCollectionParams = globals.collectionParams;
    if (showGranuleParams != null && showGranuleParams["concept_id"].length == 0) {
      showGranuleParams = null;
    }
    if (showCollectionParams !=null && showCollectionParams["concept_id"].length == 0) {
      showCollectionParams = null;
    }
    body.innerHTML = "<pre>Granule search: " + JSON.stringify(showGranuleParams, null, " ") + "</pre><br>"
        + "<pre>Collection search: " + JSON.stringify(showCollectionParams, null, " ") + "</pre><br>"
        + "<pre>Results Limit: " + globals.limit + "</pre>";

    super({ node: body });
  }
}

//
// Popup widget to display any string message
//
export class FlexiblePopupWidget extends Widget {
  constructor(text:string) {
    let body = document.createElement('div');
    body.style.display = 'flex';
    body.style.flexDirection = 'column';
    body.innerHTML = text;

    super({ node: body });
  }
}

//
// Widget with popup to set search results limit
//
export class LimitPopupWidget extends Widget {
  constructor() {
      let body = document.createElement('div');
      body.style.display = 'flex';
      body.style.flexDirection = 'column';

      super({node: body});

      this.getValue = this.getValue.bind(this);

      let inputLimit = document.createElement('input');
      inputLimit.id = 'inputLimit';
      inputLimit.value = String(globals.limit);
      this.node.appendChild(inputLimit);
  }

  /* sets limit */
  /**
   * Check for the following error cases in limit: some letters some numbers, negative number 
   * float with letters and numbers, operations/ other characters, and value greater than maximum int
   * (9007199254740991)
   * A float is automatically rounded down to the next closest integer 
   */
  getValue() {
    let limitTemp = parseInt((<HTMLInputElement>document.getElementById('inputLimit')).value);
    if (Number.isNaN(limitTemp) || limitTemp < 0) {
      Notification.error("Please enter a positive integer for results limit", {autoClose: 3000});
    } else if (limitTemp > Number.MAX_SAFE_INTEGER) {
      Notification.error("Please enter a positive integer less than 9007199254740991");
    } else {
      globals.limit = limitTemp;
    }

  }

}