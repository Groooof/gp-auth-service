function hideElement(element, duration, timeout) {
    element.style.opacity = '1';
    element.style.transition = `opacity ${duration}ms ease-out`;
    element.style.opacity = '0';
    setTimeout(() => {
        element.style.display = 'none';
    }, duration + (timeout || 0));
};

function showElement(element, duration, timeout, display) {
    element.style.opacity = '0';
    setTimeout(() => {
        element.style.display = display || 'block';
    }, timeout || 0);
    element.style.transition = `opacity ${duration}ms ease-out`;
    setTimeout(() => {
        element.style.opacity = '1';
    }, 10 + (timeout || 0));
    
};

function scrollLeft(el, px) {
    el.scrollLeft -= px || 300;
};

function scrollRight(el, px) {
    el.scrollLeft += px || 300;
};

function tableTo2dArray(table) {
    const data = [];
    const rows = table.getElementsByTagName('tr');
    for (let i = 0; i < rows.length; i++) {
        const rowData = [];
        const cells = rows[i].getElementsByTagName('td');
        for (let j = 0; j < cells.length; j++) {
            rowData.push(cells[j].textContent.trim());
        };
        data.push(rowData);
    };
    return data;
};
