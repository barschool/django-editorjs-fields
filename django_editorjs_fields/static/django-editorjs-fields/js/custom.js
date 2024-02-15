class Button {
    static get toolbox() {
        return {
            title: 'Button',
            icon: '<svg width="13" height="14" aria-hidden="true" focusable="false" data-prefix="fas" data-icon="external-link-square-alt" class="svg-inline--fa fa-external-link-square-alt fa-w-14" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path fill="currentColor" d="M448 80v352c0 26.51-21.49 48-48 48H48c-26.51 0-48-21.49-48-48V80c0-26.51 21.49-48 48-48h352c26.51 0 48 21.49 48 48zm-88 16H248.029c-21.313 0-32.08 25.861-16.971 40.971l31.984 31.987L67.515 364.485c-4.686 4.686-4.686 12.284 0 16.971l31.029 31.029c4.687 4.686 12.285 4.686 16.971 0l195.526-195.526 31.988 31.991C358.058 263.977 384 253.425 384 231.979V120c0-13.255-10.745-24-24-24z"></path></svg>'
        };
      
    }

    constructor({data, api}){
        this.data = data;
        this.api = api;

        this.nodes = {
            button: null,
            container: null,
            textHolder: null,
            textInput: null,
            hrefInput: null,
        };

        this._data = {
            text: '',
            href: {}
        };

        this.data = data;
    }
  
    render(){
        this.nodes.container = document.createElement('div');
        this.nodes.container.style = 'display: flex; padding: .7em 0;'

        this.nodes.button = document.createElement('div');
        this.nodes.button.contentEditable = true
        this.nodes.button.textContent = this.data && this.data.text ? this.data.text : '';
        this.nodes.button.style = 'background: #e94a47; padding: 15px 25px; border-radius: 5px; color: white; font-weight: bold; font-size: 15px' 

        this.nodes.hrefHolder = document.createElement('div');
        this.nodes.hrefHolder.style = 'flex: 1; margin-left: 20px;'
        
        this.nodes.hrefInputLabel = document.createElement('span');
        this.nodes.hrefInputLabel.style = 'vertical-align: middle; width: '
        this.nodes.hrefInputLabel.textContent = 'Href: '
        
        this.nodes.hrefInput = document.createElement('input');
        this.nodes.hrefInput.style = 'width: 100%'
        this.nodes.hrefInput.value = this.data && this.data.href ? this.data.href : '';

        this.nodes.hrefHolder.appendChild(this.nodes.hrefInputLabel)
        this.nodes.hrefHolder.appendChild(this.nodes.hrefInput)
        this.nodes.container.appendChild(this.nodes.button);
        this.nodes.container.appendChild(this.nodes.hrefHolder);
        return this.nodes.container
    }
  
    save(){
        return {
            text: this.nodes.button.textContent,
            href: this.nodes.hrefInput.value
        }
    }
}
window.Button = Button



class Spacer {
  static get contentless() {
    return true;
  }

  constructor({data, config, api}) {
    this.api = api;

    this._CSS = {
      block: this.api.styles.block,
      wrapper: 'ce-delimiter'
    };

    this._data = {};
    this._element = this.drawView();

    this.data = data;
  }

  drawView() {
    let div = document.createElement('DIV');
    div.classList.add('spacer');
    return div;
  }

  render() {
    return this._element;
  }

  save(toolsContent) {
    return {};
  }

  static get toolbox() {
    return {
      icon: '<svg width="13" height="14" aria-hidden="true" focusable="false" data-prefix="fas" data-icon="external-link-square-alt" class="svg-inline--fa fa-external-link-square-alt fa-w-14" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path fill="currentColor" d="M448 80v352c0 26.51-21.49 48-48 48H48c-26.51 0-48-21.49-48-48V80c0-26.51 21.49-48 48-48h352c26.51 0 48 21.49 48 48zm-88 16H248.029c-21.313 0-32.08 25.861-16.971 40.971l31.984 31.987L67.515 364.485c-4.686 4.686-4.686 12.284 0 16.971l31.029 31.029c4.687 4.686 12.285 4.686 16.971 0l195.526-195.526 31.988 31.991C358.058 263.977 384 253.425 384 231.979V120c0-13.255-10.745-24-24-24z"></path></svg>',
      title: 'Spacer'
    };
  }
}
window.Spacer = Spacer