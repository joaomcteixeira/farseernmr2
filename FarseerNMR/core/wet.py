"""
Generates nice-looking output for WET messages.

WET messages are Warnings, Errors and Troubleshooting (WETs)
messages to guide users on how to correctly proceed when facing
errors which solution is known by the Farseer-NMR community.

For more information visit:
https://github.com/Farseer-NMR/FarSeer-NMR/wiki/WET-List

The class :class:`~WetHandler` handles, configures and generates complete
WET messages. But if you want a simplified used the :func:`~generate`
straightforwardly.
"""
# Copyright © 2017-2019 Farseer-NMR
#
# @Original Article: http://bit.ly/farseerjbnmr
# @ResearchGate https://goo.gl/z8dPJU
# @Twitter https://twitter.com/farseer_nmr
# @GitHub: http://bit.ly/farseer-nmr
# @Mailist: http://bit.ly/fs_maillist
#
# This file is part of the Farseer-NMR project.
#
# Farseer-NMR is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Farseer-NMR is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Farseer-NMR. If not, see <http://www.gnu.org/licenses/>.
#
# For full list of author contributors visit:
#    https://github.com/Farseer-NMR/FarSeer-NMR/wiki/Citing
#
# Contributors to this file:
#    - João M.C. Teixeira (https://github.com/joaomcteixeira)
import textwrap

from FarseerNMR import logger

log = logger.get_log(__name__)


def generate(title, msg, wetnum, **kwargs):
    """
    Returns a formatted and complete WET message.
    
    Parameters
    ----------
    title : :obj:`str`
            The title of the message. For example: ERROR or WARNING.
        
    msg : :obj:`str`
        The WET message.
    
    wetnum : :obj:`int`
        The num of the WET message that relates to the WET list.
        See WET list at:
        https://github.com/Farseer-NMR/FarSeer-NMR/wiki/WET-List
    
    kwargs : kwargs
        Parameters to pass to :class:`~WetHandler`.
    
    Returns
    -------
    str
        The formatted and complete WET message for public display,
        according to :meth:`WetHandler.gen_wet`.
    """
    
    w = WetHandler(
        title,
        msg,
        wetnum,
        **kwargs
        )
    
    wet_message = w.gen_wet()
    
    assert isinstance(wet_message, str), "WET message NOT string"
    return wet_message


class WetHandler():
    """
    Handles generation of WET messages.
    
    Parameters
    ----------
    title : :obj:`str`
        The title of the message. For example: ERROR or WARNING.
        If request returns formatted title.
    
    msg : :obj:`str`
        The WET message.
    
    wetnum : :obj:`int`
        The num of the WET message that relates to the WET list.
        See WET list at:
        https://github.com/Farseer-NMR/FarSeer-NMR/wiki/WET-List
    
    width : :obj:`int`, optional
        The width of the wrapped and formatted message.
        Defaults to 70.
    
    style : :obj:`str`, optional
        The style char for the WET message.
        Defaults to "*".
    
    please_visit : :obj:`str`
        The "Please visit" message.
        Defaults to (obviously): "Please visit".
    
    Methods
    -------
    gen_wet
        Returns a formatted WET message according to arguments.
    """
    
    baselink = "https://github.com/Farseer-NMR/FarSeer-NMR/wiki/WET-List#wet"
    
    def __init__(
            self,
            title,
            msg,
            wetnum,
            *,
            width=70,
            style="*",
            please_visit="Please visit:",
            ):
        """
        Handles generation of wet messages.
        
        
        """
        self.title = title
        self.msg = msg
        self.wetnum = wetnum
        self.width = width
        self.style = style
        self.please_visit = please_visit
        
        return
    
    @property
    def title(self):
        """
        Formatted title.
        """
        fmt = f"{{:{self.style}^{self.width}}}\n"
        return fmt.format(f" {self._title} ")
    
    @title.setter
    def title(self, t):
        self._title = t
    
    @property
    def msg_fmt_str(self):
        """
        WET message format string.
        """
        return f"{self.style} {{:^{self.width - 4}}} {self.style}"
    
    @property
    def msg_formatted(self):
        """
        The formatted WET message.
        
        According to :attr:`~msg_fmt_str`.
        """
        return self._format_text(self.msg)
    
    @property
    def wetnum(self):
        """
        The reference WET number.
        """
        return self._wetnum
    
    @wetnum.setter
    def wetnum(self, n):
        if isinstance(n, int):
            self._wetnum = str(n)
        else:
            _ = "* ERROR * wetnum MUST be integer type"
            log.debug(_)
            raise TypeError(_)
    
    @property
    def wetlink(self):
        """
        The web page for corresponding WET number.
        """
        return self._format_text(WetHandler.baselink + self.wetnum)
    
    @property
    def spacer_line(self):
        """
        A formatted spacer line.
        """
        return self.msg_fmt_str.format(" ") + "\n"
    
    def _format_text(self, message):
        """formats a message"""
        
        message_list = list(map(
            lambda x: self.msg_fmt_str.format(x),
            textwrap.wrap(
                textwrap.dedent(message),
                width=self.width - 4,
                )
            ))
    
        return "\n".join(message_list) + "\n"
    
    def gen_wet(self):
        """
        Generates the complete WET message public formatted.
        
        Returns
        -------
        str
            The full WET message.
        """
        
        wet = \
            "\n" \
            + self.title \
            + self.msg_formatted \
            + self.spacer_line \
            + self._format_text(self.please_visit) \
            + self.wetlink  \
            + self.style * self.width \
            + "\n"
        
        return wet


if __name__ == "__main__":
    
    testmsg = generate(
        "TESTING",
        """
        This is a testing message for Farseer-NMR WET list.
        It contains several lines.
        Tabbed with triple quoted strings.
        """,
        1,
        width=50
        )
    
    print(testmsg)
