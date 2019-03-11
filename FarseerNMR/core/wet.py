"""
Generates nice-looking output for WET messages.

WET messages are Warnings, Errors and Troubleshooting
messages to guide users on how to correctly proceed when facing
errors which solution is known by the Farseer-NMR community.

For more information visit:
https://github.com/Farseer-NMR/FarSeer-NMR/wiki/WET-List
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

def generate(title, msg, wetnum, **kwargs):
    """
    Returns a formatted and complete WET message.
    
    Parameters
    ----------
    title : str
            The title of the message. For example: ERROR or WARNING.
        
    msg : str
        The WET message.
    
    wetnum : int or str
        The num of the WET message that relates to the WET list.
        See WET list at:
        https://github.com/Farseer-NMR/FarSeer-NMR/wiki/WET-List
    
    kwargs : kwargs
        Accepts kwargs to pass to :class:`~WetHanlder`.
    
    Returns
    -------
    srt
        The formatted and complete WET message for public display.
    """
    
    w = WetHandler(
        str(title),
        str(msg), 
        str(wetnum),
        **kwargs
        )
    
    wet_message = w.gen_wet()
    
    assert isinstance(wet_message, str), "WET message NOT string"
    return wet_message


class WetHandler():
    """
    Handles generation of WET messages.
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
        
        Parameters
        ----------
        title : str
            The title of the message. For example: ERROR or WARNING.
        
        msg : str
            The WET message.
        
        wetnum : int or str
            The num of the WET message that relates to the WET list.
            See WET list at:
            https://github.com/Farseer-NMR/FarSeer-NMR/wiki/WET-List
        
        width : int, optional
            The width of the wrapped and formatted message.
            Defaults to 70.
        
        style : str, optional
            The style char for the WET message.
            Defaults to "*".
        
        please_visit: str
            The "Please visit" message.
            Defaults to (obviously): "Please visit".
        
        Methods
        -------
        gen_wet
            Returns a formatted WET message according to arguments.
        
        Static Methods
        --------------
        message_fmt
            Returns a formatted message for WET display.
        """
        
        # example: '{:*^70}\n'
        self.title_fmt = f"{{:{style}^{width}}}\n"
        # example: '{:*^66}'
        self.msg_fmt = f"{style} {{:^{width - 4}}} {style}"
        
        self.spacer_line_fmt = self.msg_fmt.format(" ") + "\n"
        
        self.style = style
        self.width = width
        self.please_visit = please_visit
        
        self.title = self.title_fmt.format(f" {title} ")
        
        self.msg = self.message_fmt(self.msg_fmt, msg, width)
        
        self.wetlink = self.message_fmt(
            self.msg_fmt,
            WetHandler.baselink +  str(wetnum),
            width,
            )
        
        return
    
    @staticmethod
    def message_fmt(fmt, msg, width):
        """
        Generates a formatted message for WET display.
        
        Parameters
        ----------
        fmt : str
            The string formatter.
            For example: '{:*^66}'
        
        msg : str
            The full message for the WET display
        
        width : int
            The width of the formatted message.
        
        Returns
        -------
        str
            The formatted message with maximum width.
        """
        
        message_list = list(map(
            lambda x: fmt.format(x),
            textwrap.wrap(
                textwrap.dedent(msg),
                width=width - 4,
                )
            ))
    
        return "\n".join(message_list) + "\n"
    
    def gen_wet(self):
        
        wet = \
            "\n" \
            + self.title \
            + self.msg \
            + self.spacer_line_fmt \
            + self.message_fmt(self.msg_fmt, self.please_visit, self.width) \
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
        width=80
        )
    
    print(testmsg)
