document.addEventListener('DOMContentLoaded', function () {
    document.body.addEventListener('htmx:afterSwap', function (event) {
        console.log('htmx:afterSwap event triggered');
        if (event.detail.target.id === 'todo-list' || event.detail.target.tagName === 'LI') {
            event.detail.target.querySelectorAll('li').forEach(function (li) {
                attachEventListeners(li)
            });
        }
    });
});

function attachEventListeners(li) {
    var putButton = li.querySelector('button[hx-put]');
    var deleteButton = li.querySelector('button[hx-delete]');
    var todoInput = document.getElementById('todo-input');

    if (putButton) {
        putButton.addEventListener('click', function (e) {
            htmx.ajax('PUT', e.target.getAttribute('hx-put'), { target: li, swap: 'outerHTML' });
        });
    } else {
        console.error('Put button not found in li:', li);
    }

    if (deleteButton) {
        deleteButton.addEventListener('click', function (e) {
            htmx.ajax('DELETE', e.target.getAttribute('hx-delete'), { target: li, swap: 'outerHTML' });
        });
    } else {
        console.error('Delete button not found in li:', li);
    }

    if (todoInput) {
        todoInput.value = ''; // Clear the input field
    }
}
